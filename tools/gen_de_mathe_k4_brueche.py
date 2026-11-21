# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Brüche im Alltag – Bruchteile（Leitidee Zahl und Operation / Größen und Messen）
  python3 tools/gen_de_mathe_k4_brueche.py
Gefärbte Anteile ablesen, Bruchteile vergleichen, Bruchteile von Größen (¾ kg = 750 g, ¼ h = 15 min), Bruchteile von Mengen, Sachaufgaben.
Fehler: ¼ größer als ½ (weil 4 > 2), Anteil mit ungleichen Teilen, Bruchteil von 60 min mit 100 gerechnet.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, fr, wrap, MAL, GETEILT
from ws_common import INK, GREEN, FILL

R = random.Random(49107)
KIDS = Kids(R)


def frac(z, n):
    return fr(z, n)


def rect_svg(n, k, cols=None):
    cols = cols or n
    rows = n // cols
    w, h = 36, 30
    s = []
    cells = list(range(n))
    R.shuffle(cells)
    shaded = set(cells[:k])
    for i in range(n):
        r, c = divmod(i, cols)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (6 + c * w, 6 + r * h, w, h, FILL if i in shaded else "#ffffff", GREEN))
    return wrap(12 + cols * w, 12 + rows * h, "".join(s), "Rechteck in gleiche Teile geteilt")


def anteil():
    n = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, n - 1)
    cols = n if n <= 5 else n // 2
    pic = rect_svg(n, k, cols)
    w = [frac(n - k, n), frac(k, n - k) if n - k != k else frac(k, n + 1), frac(n, k) if k > 1 else frac(k + 1, n), frac(k, n * 2)]
    return mcq(pic + "Welcher Bruchteil ist gefärbt?", frac(k, n), [x for x in w if x != frac(k, n)],
               "Das Ganze hat %d gleich große Teile (Nenner). %d davon %s gefärbt (Zähler): <b>%s</b>." % (n, k, "ist" if k == 1 else "sind", frac(k, n)))


def vergleich():
    kind = R.choice(["stamm", "gleich_n", "gleich_z"])
    if kind == "stamm":
        a, b = R.sample([2, 3, 4, 5, 6, 8, 10], 2)
        big = frac(1, min(a, b))
        small = frac(1, max(a, b))
        return mcq("Was ist mehr: %s oder %s einer Pizza?" % (frac(1, a), frac(1, b)), big, [small, "Beides ist gleich viel", "Das kann man nicht sagen"],
                   "Je mehr Teile, desto kleiner ist jedes Teil. %s ist mehr als %s." % (big, small))
    if kind == "gleich_n":
        n = R.choice([4, 5, 6, 8, 10])
        a, b = R.sample(range(1, n), 2)
        big = frac(max(a, b), n)
        return mcq("Was ist mehr: %s oder %s?" % (frac(a, n), frac(b, n)), big, [frac(min(a, b), n), "Beides ist gleich viel", "Das kann man nicht sagen"],
                   "Gleicher Nenner, also gleich große Teile. Mehr Teile sind mehr: <b>%s</b>." % big)
    q = R.choice([(frac(1, 2), frac(2, 4)), (frac(1, 2), frac(4, 8)), (frac(1, 4), frac(2, 8)), (frac(3, 4), frac(6, 8)), (frac(1, 5), frac(2, 10))])
    return mcq("Was ist mehr: %s oder %s?" % q, "Beides ist gleich viel", [q[0], q[1], "Das kann man nicht sagen"],
               "%s und %s sind gleich viel: Teilt man die Teile noch einmal, hat man doppelt so viele, aber halb so große Teile." % q)


GROESSEN = [
    ("1 kg", 1000, "g"), ("1 m", 100, "cm"), ("1 h", 60, "min"), ("1 €", 100, "ct"), ("1 l", 1000, "ml"), ("1 km", 1000, "m"), ("1 Tag", 24, "h"), ("1 Jahr", 12, "Monate"),
]


def groesse():
    g, tot, u = R.choice(GROESSEN)
    n = R.choice([d for d in (2, 4, 5, 10, 3, 6, 8) if tot % d == 0])
    k = R.randint(1, n - 1)
    r = tot * k // n
    w = [100 * k // n if tot != 100 and 100 % n == 0 else r + tot // n, tot // n, r + tot // n if k < n - 1 else r - tot // n, k * 10]
    e = ("%s = %s %s. Durch %d teilen: %s %s %d = <b>%s %s</b>." % (g, num(tot), u, n, num(tot), GETEILT, n, num(r), u) if k == 1 else
         "%s = %s %s. Durch %d teilen und mal %d: %s %s %d = %s, %s %s %d = <b>%s %s</b>." % (g, num(tot), u, n, k, num(tot), GETEILT, n, num(tot // n), num(tot // n), MAL, k, num(r), u))
    return mcq("%s von %s = ? %s" % (frac(k, n), g, u), "%s %s" % (num(r), u), ["%s %s" % (num(x), u) for x in w if x != r and x > 0], e)


def menge():
    n = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, n - 1)
    tot = n * R.randint(2, 12)
    r = tot // n * k
    p = KIDS.next()
    thing = R.choice(["Murmeln", "Sammelkarten", "Gummibärchen", "Perlen", "Kastanien"])
    q = "%s hat %d %s. %s davon sind rot. Wie viele %s sind rot?" % (p[0], tot, thing, frac(k, n).replace("<span class='fr'>", "<span class='fr'>"), thing)
    w = [tot // n, tot - r if tot - r != r else r + 1, tot // k if k > 1 and tot % k == 0 and tot // k != r else r + n, tot * k]
    return mcq(q, "%d %s" % (r, thing), ["%d %s" % (x, thing) for x in w if x != r and x > 0],
               ("%d %s %d = <b>%d</b>." % (tot, GETEILT, n, r)) if k == 1 else "%d %s %d = %d, %d %s %d = <b>%d</b>." % (tot, GETEILT, n, tot // n, tot // n, MAL, k, r))


def sache():
    kind = R.choice(["zeit", "geld", "weg", "kuchen", "rest"])
    p = KIDS.next()
    if kind == "zeit":
        n, k = R.choice([(4, 1), (4, 3), (2, 1)])
        r = 60 * k // n
        q = "%s übt %s Klavier. Wie viele Minuten sind das?" % (p[0], {(4, 1): "eine Viertelstunde", (4, 3): "eine Dreiviertelstunde", (2, 1): "eine halbe Stunde"}[(n, k)])
        return mcq(q, "%d min" % r, ["%d min" % x for x in (100 * k // n, r + 15, r - 5 if r > 5 else r + 30) if x != r],
                   "1 Stunde = 60 min. %s von 60 min = <b>%d min</b>." % (frac(k, n), r))
    if kind == "geld":
        tot = R.choice([20, 40, 60, 80, 100])
        n, k = R.choice([(4, 1), (4, 3), (5, 1), (5, 2), (10, 3), (2, 1)])
        r = tot * k // n
        q = "%s hat %d € gespart und gibt %s davon für ein Buch aus. Wie viel kostet das Buch?" % (p[0], tot, frac(k, n))
        return mcq(q, "%d €" % r, ["%d €" % x for x in (tot // n, tot - r, r + tot // n) if x != r and x > 0],
                   "%d € %s %d = %d €, %d € %s %d = <b>%d €</b>." % (tot, GETEILT, n, tot // n, tot // n, MAL, k, r))
    if kind == "weg":
        tot = R.choice([400, 800, 1000, 1200, 2000])
        n, k = R.choice([(4, 1), (4, 3), (2, 1), (5, 2), (10, 7)])
        r = tot * k // n
        q = "Der Schulweg ist %s m lang. %s hat schon %s geschafft. Wie viele Meter sind das?" % (num(tot), p[0], frac(k, n))
        return mcq(q, "%s m" % num(r), ["%s m" % num(x) for x in (tot // n, tot - r, r + 100) if x != r],
                   "%s m %s %d %s %d = <b>%s m</b>." % (num(tot), GETEILT, n, MAL, k, num(r)))
    if kind == "kuchen":
        n = R.choice([8, 12, 16])
        k = R.choice([d for d in (1, 2, 3) if n % 4 == 0])
        eaten = n * k // 4
        q = "Ein Kuchen ist in %d gleich große Stücke geschnitten. %s des Kuchens wird gegessen. Wie viele Stücke sind das?" % (n, frac(k, 4))
        return mcq(q, "%d Stücke" % eaten, ["%d Stücke" % x for x in (k, n - eaten, eaten + 1) if x != eaten and x > 1],
                   "%d %s 4 = %d Stücke sind ein Viertel. %s sind <b>%d Stücke</b>." % (n, GETEILT, n // 4, frac(k, 4), eaten))
    tot = R.choice([24, 36, 48, 60])
    q = "In der Klasse sind %d Kinder. Die Hälfte fährt mit dem Rad, ein Viertel kommt zu Fuß, der Rest mit dem Bus. Wie viele Kinder fahren mit dem Bus?" % tot
    r = tot - tot // 2 - tot // 4
    return mcq(q, "%d Kinder" % r, ["%d Kinder" % x for x in (tot // 2, tot // 4 + 1, tot - tot // 4) if x != r],
               "Hälfte: %d, Viertel: %d. %d − %d − %d = <b>%d</b>." % (tot // 2, tot // 4, tot, tot // 2, tot // 4, r))


def main():
    seen = set()
    sets = [
        ("Welcher Teil ist gefärbt?", mix(R, seen, [(anteil, 20)])),
        ("Bruchteile vergleichen", mix(R, seen, [(vergleich, 20)])),
        ("Bruchteile von Größen", mix(R, seen, [(groesse, 20)])),
        ("Bruchteile von Mengen", mix(R, seen, [(menge, 20)])),
        ("Sachaufgaben mit Brüchen", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein Bruch beschreibt einen Teil von einem Ganzen. Der <b>Nenner</b> (unten) sagt, in wie viele gleich große Teile das Ganze geteilt ist. Der <b>Zähler</b> (oben) sagt, wie viele Teile gemeint sind.",
         "Je größer der Nenner, desto kleiner die Teile: %s ist weniger als %s." % (fr(1, 4), fr(1, 2)),
         "Einen Bruchteil einer Größe berechnest du so: durch den Nenner teilen, mal den Zähler nehmen.",
         "Merke: %s h = 15 min, %s kg = 500 g, %s m = 75 cm." % (fr(1, 4), fr(1, 2), fr(3, 4))],
        [example("%s von 1 kg" % fr(3, 4), ["1 kg = 1000 g", "1000 g %s 4 = 250 g" % GETEILT, "250 g %s 3 = 750 g" % MAL], "750 g"),
         example("%s von 24 Murmeln" % fr(2, 3), ["24 %s 3 = 8" % GETEILT, "8 %s 2 = 16" % MAL], "16 Murmeln")],
        [["%s ist mehr als %s, weil 4 größer als 2 ist" % (fr(1, 4), fr(1, 2)), "Mehr Teile heißt kleinere Teile: %s &lt; %s" % (fr(1, 4), fr(1, 2))],
         ["%s h = 25 min" % fr(1, 4), "1 h hat 60 min: 60 : 4 = 15 min"],
         ["Ungleiche Teile als Bruch zählen", "Für einen Bruch müssen alle Teile gleich groß sein"]])
    faq = [
        {"q": "Lernen Kinder in Klasse 4 schon Brüche?", "a": "In vielen Bundesländern werden in Klasse 4 einfache Bruchteile wie ein Halb, ein Viertel und drei Viertel behandelt, vor allem bei Größen wie Zeit, Gewicht und Länge. Das Rechnen mit Brüchen folgt ab Klasse 5 oder 6."},
        {"q": "Was ist der Unterschied zwischen Zähler und Nenner?", "a": "Der Nenner (unten) nennt die Anzahl der gleich großen Teile, der Zähler (oben) zählt, wie viele davon gemeint sind."},
        {"q": "Warum ist ein Viertel weniger als ein Halb?", "a": "Teilt man eine Pizza in vier Teile, sind die Stücke kleiner, als wenn man sie in zwei Teile teilt."},
        {"q": "Wo begegnen Kindern Brüche im Alltag?", "a": "Bei der Uhr (Viertelstunde), beim Einkaufen (ein halbes Kilo), beim Kuchenteilen und bei Rezepten."},
    ]
    make_unit(R, "brueche-im-alltag", "Z",
              "Die Schülerinnen und Schüler beschreiben einfache Bruchteile (Hälfte, Drittel, Viertel, Achtel, Zehntel) an Figuren, Mengen und Größen, vergleichen sie und nutzen sie in Sachsituationen (Zusammenfassung).",
              "Brüche im Alltag: Halbe, Viertel und Achtel",
              "Brüche Klasse 4 – Bruchteile von Größen, Arbeitsblätter mit Lösungen",
              "Brüche im Alltag",
              "Klasse 4: Bruchteile ablesen und vergleichen, Bruchteile von Größen (¾ kg, ¼ h) und Mengen, Sachaufgaben mit Brüchen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Nenner: in wie viele Teile? Zähler: wie viele Teile?",
              "Bruchteil einer Größe: durch den Nenner teilen, mal den Zähler.",
              body, faq, sets, 7, grade="klasse-4")


if __name__ == "__main__":
    main()
