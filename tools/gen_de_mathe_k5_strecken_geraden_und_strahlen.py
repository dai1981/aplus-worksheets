# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Strecken, Geraden und Strahlen（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k5_strecken_geraden_und_strahlen.py
Strecke, Strahl, Gerade unterscheiden, Strecken auf Karopapier messen, parallel und senkrecht (∥, ⊥), Abstand eines Punktes von einer Geraden, Anzahl von Strecken und Geraden.
Fehler: Strahl und Gerade verwechselt, Kästchen als Zentimeter gezählt (1 Kästchen = 0,5 cm), schräg gemessen statt senkrecht (Abstand).
"""
import random
from de_common import mcq, num, dez, lesson, example, make_unit, mix, MAL, table, wrap, line, text, INK, RED, BLUE, GRAY

R = random.Random(49512)
C = 22  # px pro Kästchen
LET = ["AB", "CD", "EF", "PQ", "RS", "UV", "GH", "KL", "MN"]


def grid(wc, hc):
    s = ["<rect x='0' y='0' width='%d' height='%d' fill='#fff'/>" % (wc * C, hc * C)]
    for i in range(wc + 1):
        s.append(line(i * C, 0, i * C, hc * C, "#c9d6e8", 1))
    for j in range(hc + 1):
        s.append(line(0, j * C, wc * C, j * C, "#c9d6e8", 1))
    return s


def pt(x, y, lab, col=INK, dx=0, dy=-9):
    return "<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (x * C, y * C, col) + text(x * C + dx, y * C + dy, lab, 15, col=col)


def ext(x1, y1, x2, y2, wc, hc):
    """Punkt am Rand in Richtung (x1,y1)->(x2,y2)"""
    dx, dy = x2 - x1, y2 - y1
    t = 1e9
    for v, d, hi in ((x2, dx, wc), (y2, dy, hc)):
        if d > 0:
            t = min(t, (hi - v) / float(d))
        elif d < 0:
            t = min(t, (0 - v) / float(d))
    return x2 + dx * t, y2 + dy * t


def figur(kind, P, Q, wc=14, hc=7, lab="AB"):
    s = grid(wc, hc)
    a, b = P, Q
    s1, s2 = a, b
    if kind in ("strahl", "gerade"):
        s2 = ext(a[0], a[1], b[0], b[1], wc, hc)
    if kind == "gerade":
        s1 = ext(b[0], b[1], a[0], a[1], wc, hc)
    s.append(line(s1[0] * C, s1[1] * C, s2[0] * C, s2[1] * C, BLUE, 3))
    s.append(pt(a[0], a[1], lab[0]) + pt(b[0], b[1], lab[1]))
    return wrap(wc * C, hc * C, "".join(s), "Linie durch zwei Punkte auf Karopapier", lg=True)


def zwei_pkt(wc=14, hc=7):
    while True:
        a = (R.randint(2, wc - 2), R.randint(1, hc - 1))
        b = (R.randint(2, wc - 2), R.randint(1, hc - 1))
        if abs(a[0] - b[0]) >= 4 and a != b:
            return a, b


NAME = {"strecke": "Strecke", "strahl": "Strahl", "gerade": "Gerade"}


def art():
    kind = R.choice(["strecke", "strahl", "gerade"])
    lab = R.choice(LET)
    a, b = zwei_pkt()
    q = figur(kind, a, b, lab=lab) + "Was ist die blaue Linie? (Die Linie endet nur dort, wo ein Punkt ist.)"
    ans = {"strecke": "eine Strecke %s" % lab, "strahl": "ein Strahl mit Anfangspunkt %s" % lab[0], "gerade": "eine Gerade durch %s und %s" % (lab[0], lab[1])}
    allx = list(ans.values()) + ["ein Strahl mit Anfangspunkt %s" % lab[1]]
    why = {"strecke": "Sie hat zwei Endpunkte %s und %s." % (lab[0], lab[1]), "strahl": "Sie beginnt in %s und geht über %s hinaus ohne Ende weiter." % (lab[0], lab[1]),
           "gerade": "Sie geht in beide Richtungen ohne Ende weiter."}
    return mcq(q, ans[kind], [x for x in allx if x != ans[kind]], why[kind] + " Es ist <b>%s</b>." % ans[kind])


def wissen():
    k = R.choice(["end_strecke", "end_strahl", "end_gerade", "zwei", "zeichen_par", "zeichen_senk", "laenger", "messen", "schnitt", "par_schnitt", "licht", "seil", "kante", "senk_winkel", "abstand_def"])
    D = {
        "end_strecke": ("Wie viele Endpunkte hat eine Strecke?", "2", ["1", "0", "unendlich viele"], "Eine Strecke beginnt und endet in einem Punkt: <b>2</b> Endpunkte."),
        "end_strahl": ("Wie viele Endpunkte hat ein Strahl?", "1 (den Anfangspunkt)", ["2", "0", "3"], "Ein Strahl hat einen Anfangspunkt und geht dann ohne Ende weiter: <b>1</b>."),
        "end_gerade": ("Wie viele Endpunkte hat eine Gerade?", "keinen", ["1", "2", "4"], "Eine Gerade geht in beide Richtungen ohne Ende weiter: <b>keinen</b> Endpunkt."),
        "zwei": ("Wie viele Geraden gibt es durch zwei verschiedene Punkte A und B?", "genau eine", ["genau zwei", "keine", "unendlich viele"], "Durch zwei Punkte gibt es <b>genau eine</b> Gerade."),
        "zeichen_par": ("Was bedeutet g ∥ h?", "g ist parallel zu h.", ["g ist senkrecht zu h.", "g ist so lang wie h.", "g schneidet h."], "Das Zeichen ∥ heißt <b>parallel</b>."),
        "zeichen_senk": ("Was bedeutet g ⊥ h?", "g ist senkrecht zu h.", ["g ist parallel zu h.", "g ist länger als h.", "g und h haben keinen Punkt gemeinsam."], "Das Zeichen ⊥ heißt <b>senkrecht</b> (rechter Winkel)."),
        "laenger": ("Welche Linie kann man mit dem Lineal ganz messen?", "eine Strecke", ["einen Strahl", "eine Gerade", "jede Linie"], "Nur eine <b>Strecke</b> hat eine Länge. Strahl und Gerade sind unendlich lang."),
        "messen": ("Die Strecke AB ist 6 cm lang. Wie schreibt man das?", "|AB| = 6 cm", ["AB = 6", "|A| + |B| = 6 cm", "AB ∥ 6 cm"], "Die Länge der Strecke schreibt man mit Strichen: <b>|AB| = 6 cm</b>."),
        "schnitt": ("Zwei Geraden sind nicht parallel. Wie viele Schnittpunkte haben sie?", "genau einen", ["keinen", "zwei", "unendlich viele"], "Nicht parallele Geraden schneiden sich in <b>genau einem</b> Punkt."),
        "par_schnitt": ("Zwei verschiedene Geraden sind parallel. Wie viele Schnittpunkte haben sie?", "keinen", ["genau einen", "zwei", "unendlich viele"], "Parallele Geraden haben überall denselben Abstand: <b>keinen</b> Schnittpunkt."),
        "licht": ("Ein Lichtstrahl geht von einer Taschenlampe aus. Welches Modell passt am besten?", "ein Strahl", ["eine Strecke", "eine Gerade", "ein Punkt"], "Er hat einen Anfang (die Lampe), aber kein Ende: <b>ein Strahl</b>."),
        "seil": ("Ein Seil ist zwischen zwei Bäumen gespannt. Welches Modell passt am besten?", "eine Strecke", ["ein Strahl", "eine Gerade", "zwei Strahlen"], "Das Seil hat zwei Enden: <b>eine Strecke</b>."),
        "kante": ("Die Kante eines Tisches ist ein Beispiel für …", "eine Strecke", ["einen Strahl", "eine Gerade", "einen Punkt"], "Die Kante hat zwei Enden: <b>eine Strecke</b>."),
        "senk_winkel": ("Zwei Geraden sind senkrecht zueinander. Welchen Winkel bilden sie?", "90°", ["180°", "45°", "360°"], "Senkrecht heißt: Sie bilden einen rechten Winkel, <b>90°</b>."),
        "abstand_def": ("Wie misst man den Abstand eines Punktes P von einer Geraden g?", "auf der Senkrechten von P zu g", ["auf irgendeiner Linie von P zu g", "parallel zu g", "von P bis zum Rand des Blattes"], "Der Abstand ist die kürzeste Verbindung: <b>auf der Senkrechten</b> von P zu g."),
    }
    q, a, w, e = D[k]
    return mcq(q, a, w, e)


def messen():
    wc, hc = 16, 5
    s = grid(wc, hc)
    lab = R.choice(LET)
    kind = R.choice(["h", "h", "v"])
    if kind == "h":
        n = R.randint(3, 14)
        x0 = R.randint(1, wc - 1 - n)
        y = R.randint(1, hc - 1)
        a, b = (x0, y), (x0 + n, y)
    else:
        wc, hc = 10, 10
        s = grid(wc, hc)
        n = R.randint(3, 9)
        y0 = R.randint(1, hc - 1 - n)
        x = R.randint(2, wc - 2)
        a, b = (x, y0), (x, y0 + n)
    s.append(line(a[0] * C, a[1] * C, b[0] * C, b[1] * C, BLUE, 3))
    s.append(pt(a[0], a[1], lab[0], dx=(0 if kind == "h" else -12), dy=(-9 if kind == "h" else 5)) + pt(b[0], b[1], lab[1], dx=(0 if kind == "h" else -12), dy=(-9 if kind == "h" else 5)))
    q = wrap(wc * C, hc * C, "".join(s), "Strecke auf Karopapier") + "Ein Kästchen ist 5 mm breit. Wie lang ist die Strecke %s?" % lab
    cm = dez(n / 2.0) + " cm"
    return mcq(q, cm, ["%d cm" % n, "%d mm" % n, dez(n / 2.0 + 0.5) + " cm"], "%d Kästchen %s 5 mm = %d mm = <b>%s</b>." % (n, MAL, 5 * n, cm))


def lage():
    wc, hc = 14, 8
    s = grid(wc, hc)
    kind = R.choice(["par", "senk", "weder"])
    dirs = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2), (2, -1), (1, -2)]
    d = R.choice(dirs)
    if kind == "par":
        e = d
    elif kind == "senk":
        e = (-d[1], d[0])
    else:
        e = R.choice([x for x in dirs if x != d and x != (-d[0], -d[1]) and x[0] * d[0] + x[1] * d[1] != 0 and x[0] * d[1] != x[1] * d[0]])
    def lin(p, v, col, nm):
        q1 = ext(p[0], p[1], p[0] + v[0], p[1] + v[1], wc, hc)
        q0 = ext(p[0] + v[0], p[1] + v[1], p[0], p[1], wc, hc)
        lx, ly = q1
        return line(q0[0] * C, q0[1] * C, q1[0] * C, q1[1] * C, col, 3) + text(min(max(lx * C, 12), wc * C - 12), min(max(ly * C - 6, 16), hc * C - 6), nm, 16, col=col)
    p1 = (R.randint(3, 5), R.randint(3, 5))
    p2 = (p1[0] + R.randint(4, 6), p1[1] + R.choice([-1, 0, 1, 2]))
    if kind == "par" and (p2[0] - p1[0]) * d[1] == (p2[1] - p1[1]) * d[0]:
        return None
    s.append(lin(p1, d, BLUE, "g") + lin(p2, e, RED, "h"))
    q = wrap(wc * C, hc * C, "".join(s), "zwei Geraden g und h auf Karopapier", lg=True) + "Wie liegen die Geraden g und h zueinander?"
    ans = {"par": "g ∥ h (parallel)", "senk": "g ⊥ h (senkrecht)", "weder": "weder parallel noch senkrecht"}
    why = {"par": "Beide gehen in dieselbe Richtung (gleiche Kästchenschritte) und schneiden sich nie.",
           "senk": "Dreht man die Kästchenschritte von g um 90°, bekommt man die Schritte von h. Sie bilden einen rechten Winkel.",
           "weder": "Sie schneiden sich, aber nicht im rechten Winkel."}
    return mcq(q, ans[kind], [v for k2, v in ans.items() if k2 != kind] + ["g und h sind gleich lang"], why[kind] + " <b>%s</b>." % ans[kind])


def abstand():
    wc, hc = 14, 9
    s = grid(wc, hc)
    y = R.randint(6, 8)
    s.append(line(0, y * C, wc * C, y * C, BLUE, 3) + text(wc * C - 12, y * C - 6, "g", 16, col=BLUE))
    px, py = R.randint(2, wc - 3), R.randint(1, y - 2)
    n = y - py
    fx = px + R.choice([-4, -3, 3, 4])
    fx = min(max(fx, 1), wc - 1)
    s.append(line(px * C, py * C, fx * C, y * C, GRAY, 2, " stroke-dasharray='5 4'"))
    s.append(pt(px, py, "P", RED))
    q = wrap(wc * C, hc * C, "".join(s), "Punkt P über einer Geraden g", lg=True) + "Ein Kästchen ist 5 mm breit. Wie groß ist der Abstand des Punktes P von der Geraden g?"
    cm = dez(n / 2.0) + " cm"
    sl = ((fx - px) ** 2 + n * n) ** 0.5 / 2.0
    w2 = dez(round(sl * 2) / 2.0) + " cm"
    return mcq(q, cm, ["%d cm" % n, w2, "%d mm" % n], "Man misst senkrecht von P zu g (nicht schräg wie die gestrichelte Linie): %d Kästchen = <b>%s</b>." % (n, cm))


def anzahl():
    kind = R.choice(["strecken", "geraden", "bild"])
    if kind in ("strecken", "geraden"):
        n = R.randint(3, 9)
        k = n * (n - 1) // 2
        wort = "Strecken" if kind == "strecken" else "Geraden"
        zus = "" if kind == "strecken" else " Keine drei Punkte liegen auf einer Geraden."
        return mcq("Auf einem Blatt liegen %d Punkte.%s Wie viele %s kann man zeichnen, die jeweils zwei dieser Punkte verbinden?" % (n, zus, wort), str(k), [str(n * (n - 1)), str(n), str(k + 1)],
                   "Jeder Punkt wird mit %d anderen verbunden: %d %s %d = %d. Jede Linie ist doppelt gezählt: <b>%d</b>." % (n - 1, n, MAL, n - 1, n * (n - 1), k))
    n = R.randint(3, 6)
    k = n * (n - 1) // 2
    return mcq("Auf einer Strecke AB liegen außer A und B noch %d weitere Punkte. Wie viele Strecken gibt es zwischen je zwei der Punkte?" % (n - 2), str(k), [str(n - 1), str(n), str(n * (n - 1))],
               "Es sind %d Punkte. %d %s %d : 2 = <b>%d</b> Strecken." % (n, n, MAL, n - 1, k))


def alltag():
    k = R.choice(range(12))
    p = [
        ("Ein Weg ist auf der Karte 6 Kästchen lang. 1 Kästchen ist 5 mm. Wie lang ist der Weg auf der Karte?", "3 cm", ["6 cm", "30 cm", "6 mm"], "6 %s 5 mm = 30 mm = <b>3 cm</b>." % MAL),
        ("Die Gleise einer Eisenbahn liegen immer im gleichen Abstand. Wie liegen die beiden Schienen zueinander?", "parallel", ["senkrecht", "sie schneiden sich", "weder parallel noch senkrecht"], "Gleicher Abstand überall: <b>parallel</b>."),
        ("Ein Fahnenmast steht auf einem ebenen Platz. Wie steht er zum Boden?", "senkrecht", ["parallel", "schräg", "gar nicht"], "Er bildet mit dem Boden einen rechten Winkel: <b>senkrecht</b>."),
        ("Lina zeichnet die Strecke AB mit |AB| = 7 cm. Dann verlängert sie die Strecke über B hinaus ohne Ende. Was hat sie jetzt gezeichnet?", "einen Strahl mit Anfangspunkt A", ["eine Gerade", "eine längere Strecke", "einen Strahl mit Anfangspunkt B"], "Er beginnt in A und hat kein Ende: <b>ein Strahl mit Anfangspunkt A</b>."),
        ("Die Strecke AB ist 9 cm lang. M ist genau in der Mitte. Wie lang ist die Strecke AM?", "4,5 cm", ["4 cm", "9 cm", "5 cm"], "9 cm : 2 = <b>4,5 cm</b>."),
        ("Auf einer Straße steht ein Haus 40 m vom Rand entfernt (senkrecht gemessen). Ein Weg zum Haus führt schräg. Kann der schräge Weg kürzer als 40 m sein?", "Nein, der senkrechte Weg ist der kürzeste.", ["Ja, schräge Wege sind kürzer.", "Ja, wenn man schnell läuft.", "Beide sind immer gleich lang."], "Der Abstand senkrecht ist immer die <b>kürzeste</b> Verbindung."),
        ("Paul legt 3 Stifte so, dass jeder zu jedem parallel ist. Wie viele Schnittpunkte gibt es?", "0", ["1", "2", "3"], "Parallele Linien schneiden sich nicht: <b>0</b>."),
        ("Drei Geraden schneiden sich paarweise, aber nie zu dritt in einem Punkt. Wie viele Schnittpunkte gibt es?", "3", ["1", "6", "2"], "Jedes Paar hat einen Schnittpunkt: 3 Paare ergeben <b>3</b>."),
        ("Ein Rechteck hat die Seiten a und b. Wie liegen zwei gegenüberliegende Seiten zueinander?", "parallel", ["senkrecht", "sie schneiden sich", "keine Aussage möglich"], "Gegenüberliegende Seiten im Rechteck sind <b>parallel</b>."),
        ("Ein Rechteck hat die Seiten a und b. Wie liegen zwei benachbarte Seiten zueinander?", "senkrecht", ["parallel", "gleich lang", "keine Aussage möglich"], "Im Rechteck gibt es nur rechte Winkel: benachbarte Seiten sind <b>senkrecht</b>."),
        ("Max zeichnet eine Gerade g und einen Punkt P, der nicht auf g liegt. Wie viele Parallelen zu g gehen durch P?", "genau eine", ["keine", "zwei", "unendlich viele"], "Durch einen Punkt gibt es <b>genau eine</b> Parallele zu g."),
        ("Ein Strahl beginnt im Punkt S und geht durch den Punkt T. Wie schreibt man ihn?", "Strahl ST (Anfangspunkt S)", ["Strahl TS", "Strecke ST", "Gerade ST"], "Der Anfangspunkt steht vorn: <b>Strahl ST</b>."),
    ]
    q, a, w, e = p[k]
    return mcq(q, a, w, e)


def main():
    seen = set()
    sets = [
        ("Strecke, Strahl oder Gerade?", mix(R, seen, [(art, 12), (wissen, 8)])),
        ("Strecken messen", mix(R, seen, [(messen, 20)])),
        ("Parallel und senkrecht", mix(R, seen, [(lage, 20)])),
        ("Abstand und Anzahl", mix(R, seen, [(abstand, 12), (anzahl, 8)])),
        ("Gemischte Aufgaben", mix(R, seen, [(wissen, 7), (alltag, 12), (anzahl, 1)])),
    ]
    body = lesson(
        ["Eine <b>Strecke</b> AB hat zwei Endpunkte A und B. Ihre Länge schreibt man |AB|.",
         "Ein <b>Strahl</b> hat einen Anfangspunkt und geht in eine Richtung ohne Ende weiter.",
         "Eine <b>Gerade</b> hat keinen Endpunkt. Sie geht in beide Richtungen ohne Ende weiter.",
         "Zwei Geraden sind <b>parallel</b> (g ∥ h), wenn sie überall denselben Abstand haben. Sie sind <b>senkrecht</b> (g ⊥ h), wenn sie einen rechten Winkel bilden.",
         "Der <b>Abstand</b> eines Punktes von einer Geraden wird immer senkrecht gemessen. Auf Karopapier ist ein Kästchen 5 mm breit."],
        [example("Strecke über 7 Kästchen", ["1 Kästchen = 5 mm", "7 %s 5 mm = 35 mm" % MAL], "3,5 cm"),
         example("Durch 4 Punkte (keine drei auf einer Geraden)", ["Jeder Punkt mit 3 anderen", "4 %s 3 = 12, doppelt gezählt" % MAL], "6 Geraden")],
        [["Strahl und Gerade verwechselt", "Gerade: kein Endpunkt, Strahl: ein Anfangspunkt"],
         ["8 Kästchen = 8 cm", "8 Kästchen = 8 %s 5 mm = 4 cm" % MAL],
         ["Abstand schräg gemessen", "Abstand immer senkrecht messen"]],
        extra=table(["Linie", "Endpunkte", "Länge"], [["Strecke", "2", "messbar"], ["Strahl", "1", "unendlich"], ["Gerade", "0", "unendlich"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen Strecke, Strahl und Gerade?", "a": "Eine Strecke hat zwei Endpunkte, ein Strahl einen Anfangspunkt und eine Gerade keinen Endpunkt."},
        {"q": "Wie zeichne ich eine Senkrechte mit dem Geodreieck?", "a": "Lege die Mittellinie des Geodreiecks auf die Gerade und zeichne an der langen Kante entlang. So entsteht ein rechter Winkel."},
        {"q": "Was bedeuten die Zeichen ∥ und ⊥?", "a": "g ∥ h heißt: g ist parallel zu h. g ⊥ h heißt: g ist senkrecht zu h."},
        {"q": "Wie misst man den Abstand eines Punktes von einer Geraden?", "a": "Man zeichnet die Senkrechte vom Punkt zur Geraden und misst diese Strecke. Das ist der kürzeste Weg."},
    ]
    make_unit(R, "strecken-geraden-und-strahlen", "R",
              "Die Schülerinnen und Schüler unterscheiden Strecken, Strahlen und Geraden, messen Strecken, erkennen parallele und senkrechte Geraden und bestimmen Abstände (Zusammenfassung).",
              "Strecken, Geraden und Strahlen",
              "Strecken, Geraden und Strahlen Klasse 5 – Arbeitsblätter",
              "Strecken & Geraden",
              "Strecken, Strahlen und Geraden für Klasse 5: unterscheiden, messen, parallel und senkrecht, Abstand eines Punktes. 100 Aufgaben mit Lösungen, kostenlos.",
              "Strecke: 2 Endpunkte. Strahl: 1. Gerade: keiner.",
              "Abstände misst man immer senkrecht.",
              body, faq, sets, 12, grade="klasse-5")


if __name__ == "__main__":
    main()
