# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Brüche vergleichen und ordnen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_brueche_vergleichen_und_ordnen.py
Gleiche Nenner, gleiche Zähler, Hauptnenner (kgV), Vergleich mit 1/2, Brüche ordnen, Brüche am Zahlenstrahl, Anteile vergleichen.
Fehler: größerer Nenner = größerer Bruch, nur die Zähler verglichen, Hauptnenner falsch (Nenner addiert).
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table, wrap, line, text, INK, RED
from de_k6 import bh, mcq

R = random.Random(49602)
KIDS = Kids(R)
LT, GT = "&lt;", "&gt;"


def lcm(a, b):
    return a * b // gcd(a, b)


def zeichen(a, b):
    return LT if a < b else GT if a > b else "="


def zwei(kind):
    while True:
        if kind == "nenner":
            n = R.randint(3, 15)
            a, b = R.sample(range(1, n), 2)
            A, B = (a, n), (b, n)
        elif kind == "zaehler":
            z = R.randint(1, 7)
            n1, n2 = R.sample(range(z + 1, z + 12), 2)
            A, B = (z, n1), (z, n2)
            if gcd(z, n1) > 1 or gcd(z, n2) > 1:
                continue
        else:
            n1, n2 = R.sample([3, 4, 5, 6, 7, 8, 9, 10, 12, 15], 2)
            A, B = (R.randint(1, n1 - 1), n1), (R.randint(1, n2 - 1), n2)
            if Fr(*A) == Fr(*B) or gcd(*A) > 1 or gcd(*B) > 1:
                continue
        return A, B


def vergleich():
    kind = R.choice(["nenner", "zaehler", "haupt", "haupt"])
    A, B = zwei(kind)
    a, b = Fr(*A), Fr(*B)
    s = zeichen(a, b)
    q = "Setze &lt;, &gt; oder = ein: %s ☐ %s" % (fr(*A), fr(*B))
    w = [x for x in (LT, GT, "=") if x != s]
    if kind == "nenner":
        e = "Gleicher Nenner: Der größere Zähler gibt den größeren Bruch. <b>%s %s %s</b>" % (fr(*A), s, fr(*B))
    elif kind == "zaehler":
        e = "Gleicher Zähler: Je größer der Nenner, desto kleiner die Teile. <b>%s %s %s</b>" % (fr(*A), s, fr(*B))
    else:
        h = lcm(A[1], B[1])
        e = "Hauptnenner %d: %s und %s. <b>%s %s %s</b>" % (h, fr(A[0] * h // A[1], h), fr(B[0] * h // B[1], h), fr(*A), s, fr(*B))
    return mcq(q, s, w + ["≈"], e)


def groesser():
    kind = R.choice(["haupt", "haupt", "zaehler"])
    A, B = zwei(kind)
    a, b = Fr(*A), Fr(*B)
    g = A if a > b else B
    h = lcm(A[1], B[1])
    return mcq("Welcher Bruch ist größer: %s oder %s?" % (fr(*A), fr(*B)), fr(*g), [fr(*(B if g == A else A)), "Beide sind gleich groß.", "Das kann man nicht vergleichen."],
               ("Hauptnenner %d: %s und %s. Größer ist <b>%s</b>." % (h, fr(A[0] * h // A[1], h), fr(B[0] * h // B[1], h), fr(*g))) if kind == "haupt" else "Gleicher Zähler, kleinerer Nenner: größere Teile. <b>%s</b>" % fr(*g))


def hauptnenner():
    n1, n2 = R.sample([2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20], 2)
    h = lcm(n1, n2)
    return mcq("Welches ist der kleinste gemeinsame Nenner (Hauptnenner) von %s und %s?" % (fr(1, n1), fr(1, n2)), str(h), [str(n1 + n2), str(n1 * n2) if n1 * n2 != h else str(h * 2), str(max(n1, n2))],
               "Kleinstes gemeinsames Vielfaches von %d und %d: <b>%d</b>." % (n1, n2, h))


def halb():
    n = R.randint(3, 16)
    z = R.randint(1, n - 1)
    if 2 * z == n:
        return None
    s = "kleiner als" if 2 * z < n else "größer als"
    return mcq("Ist %s kleiner oder größer als %s?" % (fr(z, n), fr(1, 2)), s + " " + fr(1, 2), [("größer als" if 2 * z < n else "kleiner als") + " " + fr(1, 2), "genau " + fr(1, 2), "Das kann man nicht sagen."],
               "Die Hälfte von %d ist %s. Der Zähler %d ist %s: <b>%s %s</b>." % (n, ("%d" % (n // 2)) if n % 2 == 0 else ("%d,5" % (n // 2)), z, "kleiner" if 2 * z < n else "größer", s, fr(1, 2)))


def ordnen():
    ns = R.sample([2, 3, 4, 5, 6, 8, 10, 12], 3)
    fs = []
    for n in ns:
        z = R.randint(1, n - 1)
        if gcd(z, n) > 1:
            return None
        fs.append((z, n))
    vals = [Fr(*f) for f in fs]
    if len(set(vals)) < 3:
        return None
    srt = sorted(fs, key=lambda f: Fr(*f))
    ans = " &lt; ".join(fr(*f) for f in srt)
    byn = sorted(fs, key=lambda f: f[1])
    byz = sorted(fs, key=lambda f: f[0])
    rev = list(reversed(srt))
    cands = [" &lt; ".join(fr(*f) for f in x) for x in (byn, byz, rev, [srt[1], srt[0], srt[2]])]
    return mcq("Ordne der Größe nach, beginne mit dem kleinsten Bruch: %s" % ", ".join(fr(*f) for f in fs), ans, cands,
               "Auf einen gemeinsamen Nenner bringen und die Zähler vergleichen: <b>%s</b>." % ans)


def strahl2():
    n = R.choice([3, 4, 5, 6, 8, 10, 12])
    z = R.randint(1, 2 * n - 1)
    if z == n:
        return None
    W = 420
    x0 = 30
    u = (W - 60) / (2.0 * n)
    y = 50
    s = [line(x0 - 6, y, x0 + 2 * n * u + 10, y, INK, 2)]
    for i in range(2 * n + 1):
        L = 10 if i % n == 0 else 6
        s.append(line(x0 + i * u, y - L, x0 + i * u, y + L, INK, 2 if i % n == 0 else 1.2))
    for i, t in ((0, "0"), (n, "1"), (2 * n, "2")):
        s.append(text(x0 + i * u, y + 28, t, 15))
    s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (x0 + z * u, y - 12, RED) + text(x0 + z * u, y - 27, "A", 15, col=RED))
    pic = wrap(W, y + 40, "".join(s), "Zahlenstrahl von 0 bis 2", lg=True)
    v = Fr(z, n)
    ans = bh(v, gemischt=True)
    return mcq(pic + "Welche Zahl gehört zum Punkt A?", ans, [bh(Fr(z, 2 * n), True), bh(Fr(z + 1, n), True), bh(Fr(n, z), True) if z != n else None, fr(z, 10) if n != 10 else fr(z, 12)],
               "Von 0 bis 1 sind %d gleich große Abschnitte, jeder ist %s. A liegt beim %d. Strich: <b>%s</b>%s." % (n, fr(1, n), z, fr(z, n), (" = " + ans) if z > n or v.denominator != n else ""))


def sache():
    kind = R.choice(["pizza", "test", "saft", "weg", "klasse"])
    p1, _ = KIDS.next()
    p2, _ = KIDS.next()
    if p1 == p2:
        return None
    A, B = zwei("haupt")
    a, b = Fr(*A), Fr(*B)
    g = p1 if a > b else p2
    h = lcm(A[1], B[1])
    e = "Hauptnenner %d: %s und %s. <b>%s</b>." % (h, fr(A[0] * h // A[1], h), fr(B[0] * h // B[1], h), g)
    opts = [p2 if g == p1 else p1, "Beide gleich viel.", "Das kann man nicht sagen."]
    if kind == "pizza":
        q = "%s isst %s einer Pizza, %s isst %s einer gleich großen Pizza. Wer isst mehr?" % (p1, fr(*A), p2, fr(*B))
    elif kind == "test":
        q = "Im Test hat %s %s der Aufgaben richtig, %s hat %s richtig. Wer hat den größeren Anteil richtig?" % (p1, fr(*A), p2, fr(*B))
    elif kind == "saft":
        q = "%s trinkt %s Liter Saft, %s trinkt %s Liter. Wer trinkt mehr?" % (p1, fr(*A), p2, fr(*B))
    elif kind == "weg":
        q = "%s hat %s des Weges geschafft, %s hat %s geschafft. Wer ist weiter gekommen?" % (p1, fr(*A), p2, fr(*B))
    else:
        c1 = [A[1] * k for k in range(1, 20) if 18 <= A[1] * k <= 32]
        c2 = [B[1] * k for k in range(1, 20) if 18 <= B[1] * k <= 32]
        if not c1 or not c2:
            return None
        t1, t2 = R.choice(c1), R.choice(c2)
        if t1 == t2:
            return None
        q = "In der 6a fahren %d von %d Kindern mit dem Rad, in der 6b %d von %d. In welcher Klasse ist der Anteil größer?" % (A[0] * t1 // A[1], t1, B[0] * t2 // B[1], t2)
        g = "in der 6a" if a > b else "in der 6b"
        return mcq(q, g, ["in der 6b" if a > b else "in der 6a", "in beiden gleich", "in der Klasse mit mehr Kindern"],
                   "Gekürzt: %s und %s. Hauptnenner %d: %s und %s. <b>%s</b>." % (fr(*A), fr(*B), h, fr(A[0] * h // A[1], h), fr(B[0] * h // B[1], h), g[0].upper() + g[1:]))
    return mcq(q, g, opts, e)


def main():
    seen = set()
    sets = [
        ("Gleiche Nenner oder gleiche Zähler", mix(R, seen, [(vergleich, 20)])),
        ("Hauptnenner finden", mix(R, seen, [(hauptnenner, 10), (groesser, 10)])),
        ("Vergleich mit der Hälfte und Zahlenstrahl", mix(R, seen, [(halb, 10), (strahl2, 10)])),
        ("Brüche ordnen", mix(R, seen, [(ordnen, 20)])),
        ("Anteile vergleichen", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Gleiche Nenner</b>: Der Bruch mit dem größeren Zähler ist größer.",
         "<b>Gleiche Zähler</b>: Der Bruch mit dem kleineren Nenner ist größer, denn die Teile sind größer.",
         "<b>Verschiedene Nenner</b>: Beide Brüche auf den <b>Hauptnenner</b> (kleinstes gemeinsames Vielfaches der Nenner) erweitern, dann die Zähler vergleichen.",
         "Oft hilft auch der Vergleich mit %s oder mit 1." % fr(1, 2)],
        [example("%s ☐ %s" % (fr(3, 4), fr(5, 6)), ["Hauptnenner 12", "%s und %s" % (fr(9, 12), fr(10, 12))], "%s &lt; %s" % (fr(3, 4), fr(5, 6))),
         example("%s ☐ %s" % (fr(2, 5), fr(2, 7)), ["gleicher Zähler", "Fünftel sind größer als Siebtel"], "%s &gt; %s" % (fr(2, 5), fr(2, 7)))],
        [["%s &gt; %s, weil 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Achtel sind kleiner als Viertel: %s &lt; %s" % (fr(1, 8), fr(1, 4))],
         ["%s &gt; %s, weil 3 &gt; 2" % (fr(3, 8), fr(2, 3)), "Erst gleichnamig machen: %s &lt; %s" % (fr(9, 24), fr(16, 24))],
         ["Hauptnenner von 4 und 6: 10", "Ein Vielfaches beider Nenner: 12"]])
    faq = [
        {"q": "Wie vergleicht man Brüche mit verschiedenen Nennern?", "a": "Man erweitert beide Brüche auf denselben Nenner (Hauptnenner) und vergleicht dann die Zähler."},
        {"q": "Was ist der Hauptnenner?", "a": "Das kleinste gemeinsame Vielfache (kgV) der Nenner, z. B. 12 für die Nenner 4 und 6."},
        {"q": "Warum ist 1/8 kleiner als 1/4?", "a": "Wenn man ein Ganzes in 8 Teile teilt, ist jedes Teil kleiner als bei 4 Teilen."},
        {"q": "Gibt es einen schnellen Trick?", "a": "Bei gleichen Zählern gilt: kleinerer Nenner, größerer Bruch. Oft hilft auch der Vergleich mit 1/2."},
    ]
    make_unit(R, "brueche-vergleichen-und-ordnen", "Z",
              "Die Schülerinnen und Schüler vergleichen und ordnen Brüche mit gleichen und verschiedenen Nennern, nutzen den Hauptnenner und stellen Brüche am Zahlenstrahl dar (Zusammenfassung).",
              "Brüche vergleichen und ordnen",
              "Brüche vergleichen und ordnen Klasse 6 – Arbeitsblätter mit Lösungen",
              "Brüche vergleichen",
              "Brüche vergleichen für Klasse 6: gleiche Nenner, gleiche Zähler, Hauptnenner, Zahlenstrahl und Brüche ordnen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Gleichnamig machen, dann die Zähler vergleichen.",
              "Gleicher Zähler: Der kleinere Nenner gibt den größeren Bruch.",
              body, faq, sets, 2, grade="klasse-6")


if __name__ == "__main__":
    main()
