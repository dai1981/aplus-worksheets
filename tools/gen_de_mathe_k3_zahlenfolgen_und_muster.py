# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Zahlenfolgen und Muster（Leitidee Muster, Strukturen und funktionaler Zusammenhang）
  python3 tools/gen_de_mathe_k3_zahlenfolgen_und_muster.py
Zahlenfolgen fortsetzen, Regeln erkennen, fehlende Zahlen, Zahlenmauern, wachsende Muster und Sachaufgaben.
Fehler: Regel nur aus den ersten zwei Zahlen ablesen, plus statt mal, in der Zahlenmauer subtrahiert statt addiert (oder umgekehrt).
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, wrap, MAL
from ws_common import line, text, INK, GREEN, FILL

R = random.Random(49017)
KIDS = Kids(R)


def folge():
    kind = R.choice(["plus", "plus", "minus", "mal", "wechsel"])
    if kind == "plus":
        d = R.choice([3, 4, 6, 7, 8, 9, 11, 12, 15, 20, 25, 50, 75, 100])
        s = R.randint(1, 600)
        seq = [s + i * d for i in range(5)]
        rule = "immer + %d" % d
    elif kind == "minus":
        d = R.choice([3, 4, 6, 7, 8, 9, 11, 15, 25, 50, 100])
        s = R.randint(400, 999)
        seq = [s - i * d for i in range(5)]
        rule = "immer − %d" % d
    elif kind == "mal":
        f = R.choice([2, 2, 3])
        s = R.randint(1, 9)
        seq = [s * f ** i for i in range(5)]
        rule = "immer %s %d" % (MAL, f)
    else:
        a, b = R.choice([(5, 2), (10, 3), (4, 1), (20, 5), (100, 30)])
        s = R.randint(10, 300)
        seq = [s]
        for i in range(4):
            seq.append(seq[-1] + (a if i % 2 == 0 else -b))
        rule = "abwechselnd + %d und − %d" % (a, b)
    if max(seq) > 1000 or min(seq) < 0:
        return None
    show, ans = seq[:4], seq[4]
    w = [ans + 1, ans - 1, show[3] + (show[1] - show[0]) if kind != "wechsel" else show[3] + (seq[1] - seq[0]) + 1, ans + 10, show[3] * 2 if kind != "mal" else show[3] + show[3] // 2]
    return mcq("Setze die Zahlenfolge fort: %s, ?" % ", ".join(num(x) for x in show), num(ans), [num(x) for x in w if x != ans and x > 0],
               "Regel: %s. Die nächste Zahl ist <b>%s</b>." % (rule, num(ans)))


def regel():
    kind = R.choice(["plus", "mal", "minus", "wechsel"])
    if kind == "plus":
        d = R.choice([5, 6, 7, 8, 9, 12, 15, 25])
        s = R.randint(2, 200)
        seq = [s + i * d for i in range(4)]
        ans = "immer + %d" % d
        w = ["immer + %d" % (d + 1), "immer %s 2" % MAL, "immer − %d" % d]
    elif kind == "mal":
        s = R.randint(2, 12)
        seq = [s * 2 ** i for i in range(4)]
        ans = "immer %s 2" % MAL
        w = ["immer + %d" % s, "immer + 2", "immer %s 3" % MAL]
    elif kind == "minus":
        d = R.choice([5, 8, 9, 11, 20, 50])
        s = R.randint(300, 900)
        seq = [s - i * d for i in range(4)]
        ans = "immer − %d" % d
        w = ["immer + %d" % d, "immer − %d" % (d + 1), "immer − %d" % (d * 2)]
    else:
        a, b = R.choice([(5, 2), (10, 4), (6, 3), (20, 10)])
        s = R.randint(10, 200)
        seq = [s, s + a, s + a - b, s + 2 * a - b, s + 2 * a - 2 * b]
        ans = "abwechselnd + %d und − %d" % (a, b)
        w = ["immer + %d" % (a - b), "abwechselnd + %d und − %d" % (b, a), "immer + %d" % a]
    return mcq("Welche Regel passt zur Zahlenfolge %s?" % ", ".join(num(x) for x in seq), ans, w,
               "Prüfe die Regel bei allen Zahlen, nicht nur bei den ersten beiden. Richtig: <b>%s</b>." % ans)


def luecke():
    d = R.choice([4, 6, 7, 8, 9, 15, 25, 50, 75])
    s = R.randint(10, 700)
    seq = [s + i * d for i in range(5)]
    if seq[-1] > 1000:
        return None
    k = R.randint(1, 3)
    ans = seq[k]
    shown = [num(x) if i != k else "☐" for i, x in enumerate(seq)]
    w = [ans + 1, ans - d + 1 if d > 2 else ans + 2, ans + 10, ans - 10, seq[k - 1] + d * 2]
    return mcq("Welche Zahl fehlt? %s" % ", ".join(shown), num(ans), [num(x) for x in w if x != ans and x > 0],
               "Die Zahlen werden immer um %d größer. %s + %d = <b>%s</b>." % (d, num(seq[k - 1]), d, num(ans)))


def mauer_svg(vals):
    """vals: [unten (3), mitte (2), oben (1)], None = leer"""
    bw, bh = 60, 30
    s = []
    rows = [vals[0], vals[1], vals[2]]
    for r, row in enumerate(rows):
        y = 10 + (2 - r) * bh
        ox = 10 + r * bw / 2.0
        for i, v in enumerate(row):
            x = ox + i * bw
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y, bw, bh, "#ffffff" if v is None else FILL, GREEN))
            s.append(text(x + bw / 2.0, y + 20, num(v) if v is not None else "?", 15, col=INK if v is not None else "#c0392b"))
    return wrap(3 * bw + 20, 3 * bh + 20, "".join(s), "Zahlenmauer", lg=True)


def mauer():
    a, b, c = R.randint(10, 250), R.randint(10, 250), R.randint(10, 250)
    m1, m2 = a + b, b + c
    top = m1 + m2
    if top > 1000:
        return None
    kind = R.choice(["oben", "oben", "mitte", "unten"])
    if kind == "oben":
        pic = mauer_svg([[a, b, c], [None, None], [None]])
        ans = top
        w = [a + b + c, m1 + c, top + 10, top - b]
        e = "Jeder Stein ist die Summe der zwei Steine darunter: %s + %s = %s, %s + %s = %s, %s + %s = <b>%s</b>." % (
            num(a), num(b), num(m1), num(b), num(c), num(m2), num(m1), num(m2), num(top))
        q = "Welche Zahl steht im obersten Stein?"
    elif kind == "mitte":
        pic = mauer_svg([[a, None, c], [m1, None], [None]])
        ans = b
        w = [m1 + a, a, b + 10, abs(c - a) if abs(c - a) != b else b + 1]
        e = "Unten Mitte: %s − %s = <b>%s</b>." % (num(m1), num(a), num(b))
        q = "Welche Zahl gehört in den mittleren Stein unten?"
    else:
        pic = mauer_svg([[None, b, c], [m1, m2], [top]])
        ans = a
        w = [m1 + b, top - m1, a + 10, m2 - b]
        e = "Unten links: %s − %s = <b>%s</b>." % (num(m1), num(b), num(a))
        q = "Welche Zahl gehört in den linken Stein unten?"
    return mcq(pic + q, num(ans), [num(x) for x in w if x != ans and x > 0], e)


def streichhoelzer(n):
    """n Quadrate in einer Reihe aus Hölzern"""
    k = 20
    s = []
    for i in range(n):
        x = 6 + i * k
        s.append(line(x, 6, x + k, 6, "#b5651d", 3))
        s.append(line(x, 6 + k, x + k, 6 + k, "#b5651d", 3))
        s.append(line(x, 6, x, 6 + k, "#b5651d", 3))
    s.append(line(6 + n * k, 6, 6 + n * k, 6 + k, "#b5651d", 3))
    return s, 12 + n * k


def muster_svg(kind):
    parts, x = [], 0
    for n in (1, 2, 3):
        if kind == "hoelzer":
            s, w = streichhoelzer(n)
        else:
            s, w = [], 0
            for r in range(n):
                for c in range(n):
                    s.append("<rect x='%d' y='%d' width='12' height='12' fill='%s' stroke='%s'/>" % (6 + c * 13, 6 + r * 13, FILL, GREEN))
            w = 12 + n * 13
        parts.append("<g transform='translate(%d 0)'>%s%s</g>" % (x, "".join(s), text(w / 2.0, 66, "Figur %d" % n, 11, weight=600)))
        x += w + 26
    return wrap(x, 74, "".join(parts), "wachsendes Muster: Figur 1 bis 3")


def muster():
    kind = R.choice(["hoelzer", "quadrat", "punkte", "kinder"])
    if kind == "hoelzer":
        n = R.randint(4, 10)
        r = 3 * n + 1
        return mcq(muster_svg("hoelzer") + "Wie viele Hölzer braucht man für Figur %d?" % n, str(r), [str(x) for x in (4 * n, 3 * n, r + 3) if x != r],
                   "Figur 1: 4, Figur 2: 7, Figur 3: 10. Für jedes Quadrat kommen 3 Hölzer dazu: 1 + 3 %s %d = <b>%d</b>." % (MAL, n, r))
    if kind == "quadrat":
        n = R.randint(4, 9)
        r = n * n
        return mcq(muster_svg("quadrat") + "Wie viele kleine Quadrate hat Figur %d?" % n, str(r), [str(x) for x in (n * 4, n + n, r + n, (n - 1) * (n - 1)) if x != r],
                   "Figur %d ist ein Quadrat mit %d Reihen zu je %d: %d %s %d = <b>%d</b>." % (n, n, n, n, MAL, n, r))
    if kind == "punkte":
        a, d = R.randint(2, 6), R.randint(2, 5)
        n = R.randint(5, 10)
        r = a + (n - 1) * d
        q = "Figur 1 hat %d Punkte, Figur 2 hat %d Punkte, Figur 3 hat %d Punkte. Wie viele Punkte hat Figur %d?" % (a, a + d, a + 2 * d, n)
        return mcq(q, str(r), [str(x) for x in (a + n * d, n * d, r + d, r - 1) if x != r],
                   "Es kommen immer %d Punkte dazu. Von Figur 1 bis Figur %d sind das %d Schritte: %d + %d %s %d = <b>%d</b>." % (d, n, n - 1, a, n - 1, MAL, d, r))
    p = KIDS.next()
    a, d, n = R.choice([5, 10, 20]), R.choice([2, 5, 10]), R.randint(5, 9)
    if a == d:
        return None
    r = a + (n - 1) * d
    q = "%s liest am ersten Tag %d Seiten und an jedem weiteren Tag %d Seiten mehr als am Tag davor. Wie viele Seiten liest %s am %d. Tag?" % (p[0], a, d, p[1], n)
    return mcq(q, "%d Seiten" % r, ["%d Seiten" % x for x in (a + n * d, a * n, r + d) if x != r],
               "Tag 1: %d, Tag 2: %d, Tag 3: %d … Am %d. Tag: %d + %d %s %d = <b>%d Seiten</b>." % (a, a + d, a + 2 * d, n, a, n - 1, MAL, d, r))


def main():
    seen = set()
    sets = [
        ("Zahlenfolgen fortsetzen", mix(R, seen, [(folge, 20)])),
        ("Die Regel erkennen", mix(R, seen, [(regel, 20)])),
        ("Fehlende Zahlen", mix(R, seen, [(luecke, 20)])),
        ("Zahlenmauern", mix(R, seen, [(mauer, 20)])),
        ("Wachsende Muster und Sachaufgaben", mix(R, seen, [(muster, 20)])),
    ]
    body = lesson(
        ["In einer <b>Zahlenfolge</b> gilt eine Regel, zum Beispiel immer + 25 oder immer %s 2." % MAL,
         "Finde die Regel, indem du die Nachbarzahlen vergleichst. Prüfe sie bei <b>allen</b> Zahlen.",
         "In einer <b>Zahlenmauer</b> ist jeder Stein die Summe der beiden Steine darunter. Fehlt unten ein Stein, rechnest du minus.",
         "Bei <b>wachsenden Mustern</b> überlegst du, was von Figur zu Figur dazukommt."],
        [example("120, 145, 170, 195, ?", ["145 − 120 = 25, 170 − 145 = 25", "Regel: immer + 25", "195 + 25 = 220"], "220"),
         example("Zahlenmauer: unten 40, 25, 60", ["40 + 25 = 65, 25 + 60 = 85", "65 + 85 = 150"], "oben 150")],
        [["3, 6, 12, 24: Regel + 3", "Alle Schritte prüfen: immer %s 2" % MAL],
         ["In der Zahlenmauer unten addieren statt subtrahieren", "Fehlt ein unterer Stein: oberer Stein minus Nachbarstein"],
         ["Bei Figur 10 einfach 10 Schritte zählen", "Von Figur 1 bis Figur 10 sind es nur 9 Schritte"]],
        extra=mauer_svg([[40, 25, 60], [65, 85], [150]]))
    faq = [
        {"q": "Was ist eine Zahlenmauer?", "a": "Ein Rechenformat aus Steinen: Jeder Stein ist die Summe der beiden Steine, auf denen er liegt. Sie trainiert Plus und Minus und das Erkennen von Strukturen."},
        {"q": "Wie findet man die Regel einer Zahlenfolge?", "a": "Den Unterschied zwischen benachbarten Zahlen ausrechnen. Bleibt er gleich, ist es eine Plus- oder Minusregel; verdoppelt sich die Zahl, ist es mal 2."},
        {"q": "Wozu sind Muster im Mathematikunterricht gut?", "a": "Kinder lernen, Regelmäßigkeiten zu erkennen, zu beschreiben und fortzusetzen. Das ist eine Grundlage für spätere Algebra."},
        {"q": "Welche Leitidee ist das?", "a": "Muster, Strukturen und funktionaler Zusammenhang, eine der fünf Leitideen der Bildungsstandards Mathematik für die Grundschule."},
    ]
    make_unit(R, "zahlenfolgen-und-muster", "M",
              "Die Schülerinnen und Schüler erkennen, beschreiben und setzen Zahlenfolgen und geometrische Muster fort, nutzen Strukturen wie Zahlenmauern und begründen Regeln (Zusammenfassung).",
              "Zahlenfolgen, Muster und Zahlenmauern",
              "Zahlenfolgen und Zahlenmauern Klasse 3 – Arbeitsblätter mit Lösungen",
              "Zahlenfolgen und Muster",
              "Zahlenfolgen und Muster für Klasse 3: Folgen fortsetzen, Regeln erkennen, fehlende Zahlen, Zahlenmauern und wachsende Muster. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Finde die Regel und prüfe sie bei allen Zahlen.",
              "In der Zahlenmauer ist jeder Stein die Summe der beiden darunter.",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
