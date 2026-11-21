# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Zahlenmauern und Muster（Leitidee Muster, Strukturen und funktionaler Zusammenhang）
  python3 tools/gen_de_mathe_k2_zahlenmauern_und_muster.py
Zahlenmauern (oben ausrechnen, Lücken finden), Zahlenfolgen mit Regel, Entdeckerpäckchen, Formenmuster und wachsende Muster.
Fehler: in der Zahlenmauer alle unteren Steine addiert, Regel nur aus zwei Zahlen geraten, Muster um ein Glied verschoben.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, MAL
from gen_de_mathe_k3_zahlenfolgen_und_muster import mauer_svg, muster_svg
from k_pics import shape, M
from ws_common import svg_wrap, fig, text, GREEN

R = random.Random(49217)


def mauer_oben():
    a, b, c = R.randint(2, 30), R.randint(2, 30), R.randint(2, 30)
    m1, m2 = a + b, b + c
    top = m1 + m2
    if top > 100:
        return None
    return mcq(mauer_svg([[a, b, c], [None, None], [None]]) + "Welche Zahl steht im obersten Stein?", str(top),
               [str(a + b + c), str(top + 10), str(m1 + c), str(top - 1)],
               "Jeder Stein ist die Summe der zwei Steine darunter: %d + %d = %d, %d + %d = %d, %d + %d = <b>%d</b>." % (a, b, m1, b, c, m2, m1, m2, top))


def mauer_luecke():
    a, b, c = R.randint(2, 30), R.randint(2, 30), R.randint(2, 30)
    m1, m2 = a + b, b + c
    top = m1 + m2
    if top > 100:
        return None
    kind = R.choice(["links", "mitte", "oben_mitte"])
    if kind == "links":
        return mcq(mauer_svg([[None, b, c], [m1, m2], [top]]) + "Welche Zahl gehört in den linken Stein unten?", str(a),
                   [str(m1 + b), str(top - m1), str(a + 10) if a + 10 != top - m1 else str(a + 1)],
                   "Unten links: %d − %d = <b>%d</b>." % (m1, b, a))
    if kind == "mitte":
        return mcq(mauer_svg([[a, None, c], [m1, None], [None]]) + "Welche Zahl gehört in den mittleren Stein unten?", str(b),
                   [str(m1 + a), str(a), str(b + 10)] if a != b else [str(m1 + a), str(b + 1), str(b + 10)],
                   "%d − %d = <b>%d</b>." % (m1, a, b))
    return mcq(mauer_svg([[a, b, c], [m1, None], [top]]) + "Welche Zahl gehört in den rechten Stein in der Mitte?", str(m2),
               [str(top + m1) if top + m1 <= 100 else str(m2 + 10), str(b + c + 1), str(top - c)],
               "%d + %d = <b>%d</b>. Probe: %d + %d = %d." % (b, c, m2, m1, m2, top))


def folge():
    kind = R.choice(["plus", "minus", "doppel", "wechsel"])
    if kind == "plus":
        d = R.choice([3, 4, 6, 7, 8, 9, 11, 12])
        s = R.randint(1, 30)
        seq = [s + d * i for i in range(5)]
        if seq[-1] > 100:
            return None
        rule = "+%d" % d
    elif kind == "minus":
        d = R.choice([3, 4, 6, 7, 8, 9, 11])
        s = R.randint(50, 100)
        seq = [s - d * i for i in range(5)]
        if seq[-1] < 0:
            return None
        rule = "−%d" % d
    elif kind == "doppel":
        s = R.choice([1, 2, 3, 5, 6])
        seq = [s * 2 ** i for i in range(5)]
        if seq[-1] > 100:
            return None
        rule = "verdoppeln"
    else:
        a, b = R.randint(5, 12), R.randint(2, 6)
        s = R.randint(10, 40)
        seq = [s]
        for i in range(4):
            seq.append(seq[-1] + (a if i % 2 == 0 else -b))
        if seq[-1] > 100:
            return None
        rule = "+%d, −%d" % (a, b)
    ans = seq[4]
    w = [ans + 1, ans - 1, seq[3] + (seq[3] - seq[2]) if kind == "wechsel" else ans + (seq[1] - seq[0]), ans + 10]
    return mcq("Setze die Zahlenfolge fort: %s, ?" % ", ".join(map(str, seq[:4])), str(ans), [str(x) for x in w if x >= 0 and x != ans],
               "Die Regel ist: %s. Die nächste Zahl ist <b>%d</b>." % (rule, ans))


def paeckchen():
    kind = R.choice(["plus", "minus", "mal", "gleich"])
    if kind == "plus":
        a, b = R.randint(1, 9), R.randint(2, 9)
        st = R.choice([10, 1])
        rows = [(a + st * i, b) for i in range(4)]
        if rows[-1][0] + b > 100:
            return None
        q = "Entdeckerpäckchen: %s, %d + %d = ?" % (", ".join("%d + %d = %d" % (x, y, x + y) for x, y in rows[:3]), rows[3][0], b)
        r = rows[3][0] + b
        return mcq(q, str(r), [str(r + st), str(r - st), str(r + 1) if st == 10 else str(r + 10)],
                   "Die erste Zahl wird immer um %d größer, also auch das Ergebnis: <b>%d</b>." % (st, r))
    if kind == "minus":
        a, b = R.randint(50, 99), R.randint(2, 9)
        rows = [(a, b + i) for i in range(4)]
        q = "Entdeckerpäckchen: %s, %d − %d = ?" % (", ".join("%d − %d = %d" % (x, y, x - y) for x, y in rows[:3]), a, b + 3)
        r = a - b - 3
        return mcq(q, str(r), [str(r + 2), str(r + 1), str(a - b + 3)],
                   "Es wird immer 1 mehr abgezogen, darum wird das Ergebnis immer 1 kleiner: <b>%d</b>." % r)
    if kind == "mal":
        k = R.randint(2, 9)
        q = "Entdeckerpäckchen: 1 %s %d = %d, 2 %s %d = %d, 3 %s %d = %d, 4 %s %d = ?" % (MAL, k, k, MAL, k, 2 * k, MAL, k, 3 * k, MAL, k)
        return mcq(q, str(4 * k), [str(4 * k + 1), str(3 * k + 1), str(4 + k)],
                   "Das Ergebnis wird immer um %d größer: %d + %d = <b>%d</b>." % (k, 3 * k, k, 4 * k))
    a, b = R.randint(10, 40), R.randint(10, 40)
    d = R.randint(1, 9)
    q = "Welche Aufgabe hat dasselbe Ergebnis wie %d + %d?" % (a, b)
    ans = "%d + %d" % (a + d, b - d)
    return mcq(q, ans, ["%d + %d" % (a + d, b + d), "%d + %d" % (a - d, b - d), "%d − %d" % (a + d, b - d) if a + d > b - d else "%d + %d" % (a + d, b)],
               "Wird eine Zahl um %d größer und die andere um %d kleiner, bleibt das Ergebnis gleich: <b>%s</b>." % (d, d, ans))


NAMES = {"circle": "Kreis", "square": "Quadrat", "triangle": "Dreieck"}


def formen():
    base = R.choice([["circle", "square"], ["circle", "circle", "triangle"], ["square", "triangle", "triangle"], ["triangle", "circle", "square"],
                     ["circle", "square", "square"], ["square", "square", "circle", "triangle"], ["triangle", "circle"]])
    cols = R.sample(["red", "blue", "yellow", "green"], 1) * len(base)
    n = R.randint(7, 10)
    seq = [base[i % len(base)] for i in range(n)]
    nxt = base[n % len(base)]
    sp = 40
    s = [shape(k, M + sp / 2 + i * sp, M + 22, 14, cols[0]) for i, k in enumerate(seq)]
    s.append(text(M + sp / 2 + n * sp, M + 30, "?", 22, col=GREEN))
    pic = fig(svg_wrap(2 * M + (n + 1) * sp, 2 * M + 44, "".join(s), "Muster aus Figuren"))
    ans = NAMES[nxt]
    others = [v for v in NAMES.values() if v != ans] + ["Sechseck"]
    return mcq(pic + "Welche Figur kommt als Nächstes?", ans, others,
               "Das Muster wiederholt sich: %s. Als Nächstes kommt ein <b>%s</b>." % (", ".join(NAMES[k] for k in base), ans))


def wachsen():
    kind = R.choice(["quadrat", "hoelzer", "punkte"])
    if kind == "quadrat":
        n = R.randint(4, 6)
        r = n * n
        return mcq(muster_svg("quadrat") + "Wie viele kleine Quadrate hat Figur %d?" % n, str(r), [str(4 * n), str(r + n), str((n - 1) * (n - 1))],
                   "Figur %d hat %d Reihen mit je %d: %d %s %d = <b>%d</b>." % (n, n, n, n, MAL, n, r))
    if kind == "hoelzer":
        n = R.randint(4, 8)
        r = 3 * n + 1
        return mcq(muster_svg("hoelzer") + "Wie viele Hölzer braucht man für Figur %d?" % n, str(r), [str(4 * n), str(3 * n), str(r + 3)],
                   "Figur 1: 4, Figur 2: 7, Figur 3: 10. Es kommen immer 3 Hölzer dazu: <b>%d</b>." % r)
    a, d = R.randint(2, 5), R.randint(2, 4)
    n = R.randint(4, 7)
    r = a + (n - 1) * d
    return mcq("Figur 1 hat %d Punkte, Figur 2 hat %d Punkte, Figur 3 hat %d Punkte. Wie viele Punkte hat Figur %d?" % (a, a + d, a + 2 * d, n), str(r),
               [str(r + d), str(r - d), str(n * d)], "Es kommen immer %d Punkte dazu: <b>%d</b>." % (d, r))


def main():
    seen = set()
    sets = [
        ("Zahlenmauern", mix(R, seen, [(mauer_oben, 20)])),
        ("Lücken in Zahlenmauern", mix(R, seen, [(mauer_luecke, 20)])),
        ("Zahlenfolgen", mix(R, seen, [(folge, 20)])),
        ("Entdeckerpäckchen", mix(R, seen, [(paeckchen, 20)])),
        ("Formen und wachsende Muster", mix(R, seen, [(formen, 10), (wachsen, 10)])),
    ]
    body = lesson(
        ["In einer <b>Zahlenmauer</b> ist jeder Stein die Summe der zwei Steine darunter.",
         "Fehlt unten ein Stein, rechnest du minus: oberer Stein minus Nachbarstein.",
         "Bei einer <b>Zahlenfolge</b> suchst du die Regel, zum Beispiel immer +4 oder immer verdoppeln. Prüfe die Regel an mehreren Zahlen.",
         "In <b>Entdeckerpäckchen</b> ändern sich die Aufgaben nach einem Muster. Das Muster hilft beim Rechnen."],
        [example("Zahlenmauer mit 5, 8, 3 unten", ["5 + 8 = 13", "8 + 3 = 11", "13 + 11 = 24"], "24"),
         example("Zahlenfolge 7, 11, 15, 19, ?", ["immer +4"], "23")],
        [["In der Mauer alle unteren Zahlen addieren (5 + 8 + 3 = 16)", "Immer nur die zwei Steine darunter: 24"],
         ["Die Regel nur aus den ersten zwei Zahlen raten", "An allen Zahlen prüfen"],
         ["Beim Muster ein Glied überspringen", "Das Muster in Gedanken weiter aufsagen"]])
    faq = [
        {"q": "Warum sind Zahlenmauern so beliebt?", "a": "Sie üben Plus und Minus und zeigen Strukturen: Wird ein unterer Stein größer, werden auch die Steine darüber größer."},
        {"q": "Was sind Entdeckerpäckchen?", "a": "Aufgabenreihen mit einem Muster, zum Beispiel 12 + 5, 22 + 5, 32 + 5. Die Kinder sollen das Muster entdecken und beschreiben."},
        {"q": "Welche Muster lernen Kinder in Klasse 2?", "a": "Wiederholende Muster (Formen, Farben), Zahlenfolgen mit einer Regel und wachsende Muster aus Plättchen oder Hölzern."},
        {"q": "Wie findet man die Regel einer Zahlenfolge?", "a": "Man schaut, wie man von einer Zahl zur nächsten kommt, und prüft das bei allen Zahlen."},
    ]
    make_unit(R, "zahlenmauern-und-muster", "M",
              "Die Schülerinnen und Schüler erkennen, beschreiben und nutzen Gesetzmäßigkeiten in Zahlenmauern, Zahlenfolgen, Aufgabenreihen und geometrischen Mustern und setzen Muster fort (Zusammenfassung).",
              "Zahlenmauern und Muster",
              "Zahlenmauern und Muster Klasse 2 – Arbeitsblätter mit Lösungen",
              "Zahlenmauern und Muster",
              "Zahlenmauern und Muster für Klasse 2: Zahlenmauern ausrechnen und Lücken finden, Zahlenfolgen, Entdeckerpäckchen und Formenmuster. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Jeder Stein ist die Summe der zwei Steine darunter.",
              "Regel finden, an allen Zahlen prüfen, fortsetzen.",
              body, faq, sets, 17, grade="klasse-2")


if __name__ == "__main__":
    main()
