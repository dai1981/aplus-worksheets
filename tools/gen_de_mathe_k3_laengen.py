# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Längen – mm, cm, m und km（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k3_laengen.py
Umwandeln, gemischte Angaben (2 m 35 cm), am Lineal messen, vergleichen und rechnen, schätzen und Sachaufgaben.
Fehler: 1 m = 10 cm, 2 m 5 cm = 25 cm, am Lineal bei 1 statt bei 0 anfangen, unpassende Einheit beim Schätzen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, wrap, NB, table
from ws_common import line, text, INK, GREEN, FILL, BLUE

R = random.Random(49012)
KIDS = Kids(R)


def u(v, e):
    return "%s%s%s" % (num(v), NB, e)


def lineal(start_mm, length_mm, cm=12):
    """Lineal von 0 bis cm Zentimetern, darüber ein Streifen von start_mm bis start_mm + length_mm"""
    k = 3.4
    x0 = 16
    W = x0 * 2 + cm * 10 * k
    s = ["<rect x='%.1f' y='44' width='%.1f' height='40' fill='#fdf6d8' stroke='%s' stroke-width='1.5'/>" % (x0 - 8, cm * 10 * k + 16, INK)]
    for m in range(cm * 10 + 1):
        h = 16 if m % 10 == 0 else 11 if m % 5 == 0 else 6
        s.append(line(x0 + m * k, 44, x0 + m * k, 44 + h, INK, 1.4 if m % 10 == 0 else 0.8))
        if m % 10 == 0:
            s.append(text(x0 + m * k, 78, str(m // 10), 12, weight=600))
    s.append("<rect x='%.1f' y='18' width='%.1f' height='18' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (x0 + start_mm * k, length_mm * k, FILL, GREEN))
    s.append(line(x0 + start_mm * k, 18, x0 + start_mm * k, 44, BLUE, 1, " stroke-dasharray='3 2'"))
    s.append(line(x0 + (start_mm + length_mm) * k, 18, x0 + (start_mm + length_mm) * k, 44, BLUE, 1, " stroke-dasharray='3 2'"))
    return wrap(W, 92, "".join(s), "Lineal in Zentimetern mit einem Streifen", lg=True)


def cm_mm(mm):
    c, m = divmod(mm, 10)
    if c and m:
        return "%d%scm %d%smm" % (c, NB, m, NB)
    if c:
        return u(c, "cm")
    return u(m, "mm")


def m_cm(cm):
    a, b = divmod(cm, 100)
    if a and b:
        return "%d%sm %d%scm" % (a, NB, b, NB)
    return u(a, "m") if a else u(b, "cm")


def umwandeln():
    kind = R.choice(["m-cm", "cm-mm", "cm-m", "mm-cm", "km-m"])
    if kind == "m-cm":
        v = R.randint(2, 9)
        return mcq("%s = ? cm" % u(v, "m"), u(v * 100, "cm"), [u(x, "cm") for x in (v * 10, v * 1000, v + 100)],
                   "1 m = 100 cm. %d m = <b>%d cm</b>." % (v, v * 100))
    if kind == "cm-mm":
        v = R.randint(2, 30)
        return mcq("%s = ? mm" % u(v, "cm"), u(v * 10, "mm"), [u(x, "mm") for x in (v * 100, v + 10, v)],
                   "1 cm = 10 mm. %d cm = <b>%d mm</b>." % (v, v * 10))
    if kind == "cm-m":
        v = R.randint(2, 9)
        return mcq("%s = ? m" % u(v * 100, "cm"), u(v, "m"), [u(x, "m") for x in (v * 10, v * 100, v * 1000)],
                   "100 cm = 1 m. %d cm = <b>%d m</b>." % (v * 100, v))
    if kind == "mm-cm":
        v = R.randint(2, 40)
        return mcq("%s = ? cm" % u(v * 10, "mm"), u(v, "cm"), [u(x, "cm") for x in (v * 10, v * 100, v + 10)],
                   "10 mm = 1 cm. %d mm = <b>%d cm</b>." % (v * 10, v))
    v = R.choice([100, 200, 250, 500, 750])
    q = R.choice(["1 km = ? m", "Wie viele Meter sind ein halber Kilometer?", "1 km − %d m = ? m" % v])
    if q == "1 km = ? m":
        return mcq(q, u(1000, "m"), [u(x, "m") for x in (100, 10, 10000)], "1 km = <b>1000 m</b>.")
    if q.startswith("Wie viele"):
        return mcq(q, u(500, "m"), [u(x, "m") for x in (50, 5000, 250)], "1 km = 1000 m. Die Hälfte sind <b>500 m</b>.")
    return mcq(q, u(1000 - v, "m"), [u(x, "m") for x in (1000 + v, 100 - v // 10 if v < 1000 else 0, 900 - v if v < 900 else 50) if x > 0],
               "1 km = 1000 m. 1000 m − %d m = <b>%d m</b>." % (v, 1000 - v))


def gemischt():
    kind = R.choice(["mcm", "cmmm", "rueck"])
    if kind == "mcm":
        a, b = R.randint(1, 9), R.choice([R.randint(1, 9), R.randint(10, 99)])
        tot = a * 100 + b
        w = [int("%d%d" % (a, b)), a * 10 + b, a * 1000 + b, tot + 10]
        return mcq("%d%sm %d%scm = ? cm" % (a, NB, b, NB), u(tot, "cm"), [u(x, "cm") for x in w if x != tot],
                   "%d m = %d cm, dazu %d cm: <b>%d cm</b>." % (a, a * 100, b, tot))
    if kind == "cmmm":
        a, b = R.randint(1, 20), R.randint(1, 9)
        tot = a * 10 + b
        w = [a * 100 + b, a + b, tot + 10, int("%d0%d" % (a, b))]
        return mcq("%d%scm %d%smm = ? mm" % (a, NB, b, NB), u(tot, "mm"), [u(x, "mm") for x in w if x != tot],
                   "%d cm = %d mm, dazu %d mm: <b>%d mm</b>." % (a, a * 10, b, tot))
    tot = R.randint(101, 999)
    if tot % 100 == 0:
        return None
    a, b = divmod(tot, 100)
    w = ["%d%sm %d%scm" % (b, NB, a, NB) if b < 100 and b else None, "%d%sm %d%scm" % (a * 10 + b // 10, NB, b % 10, NB),
         "%d%sm %d%scm" % (a + 1, NB, b, NB), "%d%sm %d%scm" % (a, NB, b + 10 if b + 10 < 100 else b - 10, NB)]
    return mcq("%s = ? m ? cm" % u(tot, "cm"), m_cm(tot), [x for x in w if x and x != m_cm(tot)],
               "100 cm = 1 m. %d cm = <b>%s</b>." % (tot, m_cm(tot)))


def messen():
    start = R.choice([0, 0, 0, 10, 20, 30])
    L = R.randint(15, 90)
    if start + L > 115:
        return None
    w = [cm_mm(L + 10), cm_mm(start + L) if start else cm_mm(L - 10), cm_mm(L + 1), cm_mm(L - 1)]
    pic = lineal(start, L)
    hint = " Der Streifen beginnt nicht bei 0!" if start else ""
    return mcq(pic + "Wie lang ist der Streifen?" + (" Achte auf den Anfang." if start else ""), cm_mm(L),
               [x for x in w if x != cm_mm(L)],
               "Zähle die Zentimeter und Millimeter vom Anfang bis zum Ende des Streifens.%s Er ist <b>%s</b> lang." % (hint, cm_mm(L)))


def vergleichen():
    kind = R.choice(["groesser", "rechnen", "rechnen"])
    if kind == "groesser":
        a = R.randint(2, 9)
        b = a * 100 + R.choice([-30, -10, 20, 50, -50])
        if b == a * 100:
            return None
        big = "%s" % u(a, "m") if a * 100 > b else u(b, "cm")
        return mcq("Was ist länger: %s oder %s?" % (u(a, "m"), u(b, "cm")), big,
                   [u(b, "cm") if big == u(a, "m") else u(a, "m"), "Beide sind gleich lang", "Das kann man nicht vergleichen"],
                   "Gleiche Einheit: %d m = %d cm. %d cm %s %d cm, also ist <b>%s</b> länger." % (a, a * 100, a * 100, "&gt;" if a * 100 > b else "&lt;", b, big))
    k = R.choice(["m-cm", "cm-mm", "plus"])
    if k == "m-cm":
        c = R.randint(5, 95)
        r = 100 - c
        return mcq("1%sm − %s = ?" % (NB, u(c, "cm")), u(r, "cm"), [u(x, "cm") for x in (100 + c, r + 10, c, r - 10 if r > 10 else r + 1) if x > 0 and x != r],
                   "1 m = 100 cm. 100 cm − %d cm = <b>%d cm</b>." % (c, r))
    if k == "cm-mm":
        c = R.randint(1, 9)
        a = R.randint(2, 9)
        r = a * 10 - c
        return mcq("%s − %s = ?" % (u(a, "cm"), u(c, "mm")), u(r, "mm"), [u(x, "mm") for x in (a - c if a > c else a * 10 + c, r + 10, a * 10 + c, r - 1)],
                   "%d cm = %d mm. %d mm − %d mm = <b>%d mm</b>." % (a, a * 10, a * 10, c, r))
    a, b = R.randint(110, 450), R.randint(30, 450)
    r = a + b
    return mcq("%s + %s = ? (in cm)" % (u(a, "cm"), u(b, "cm")), u(r, "cm"), [u(x, "cm") for x in (r + 10, r - 10, r + 100)],
               "%d cm + %d cm = <b>%d cm</b> = %s." % (a, b, r, m_cm(r)))


SCHAETZ = [
    ("Wie lang ist ein Bleistift ungefähr?", 17, "cm", ["mm", "m", "km"]),
    ("Wie lang ist eine Ameise ungefähr?", 5, "mm", ["cm", "m", "km"]),
    ("Wie hoch ist eine Tür ungefähr?", 2, "m", ["cm", "mm", "km"]),
    ("Wie lang ist ein Fußballfeld ungefähr?", 100, "m", ["cm", "km", "mm"]),
    ("Wie breit ist ein Fingernagel ungefähr?", 1, "cm", ["m", "km", "mm"]),
    ("Wie lang ist ein Schulheft ungefähr?", 30, "cm", ["m", "mm", "km"]),
    ("Wie weit ist es mit dem Auto von Berlin nach Hamburg ungefähr?", 290, "km", ["m", "cm", "mm"]),
    ("Wie lang ist ein Klassenzimmer ungefähr?", 8, "m", ["km", "cm", "mm"]),
    ("Wie lang ist ein Marienkäfer ungefähr?", 7, "mm", ["cm", "m", "km"]),
    ("Wie lang ist ein Linienbus ungefähr?", 12, "m", ["cm", "km", "mm"]),
]


def sache():
    kind = R.choice(["schaetz", "schaetz", "sprung", "band", "staffel"])
    p = KIDS.next()
    if kind == "schaetz":
        qq, v, e, others = R.choice(SCHAETZ)
        return mcq(qq, u(v, e), [u(v, o) for o in others],
                   "Stell es dir vor und vergleiche mit bekannten Längen (Fingerbreite ≈ 1 cm, großer Schritt ≈ 1 m). Passend ist etwa <b>%s</b>." % u(v, e))
    if kind == "sprung":
        a, b = R.randint(180, 320), R.randint(180, 320)
        if a == b:
            return None
        p2 = KIDS.next()
        q = "Beim Weitsprung springt %s %s, %s springt %s. Wie viel weiter springt %s?" % (p[0], m_cm(a), p2[0], m_cm(b), p[0] if a > b else p2[0])
        r = abs(a - b)
        return mcq(q, u(r, "cm"), [u(x, "cm") for x in (a + b, r + 10, r + 100, abs(a // 100 * 100 - b) if a // 100 * 100 != b else r + 1) if x != r],
                   "%d cm − %d cm = <b>%d cm</b>." % (max(a, b), min(a, b), r))
    if kind == "band":
        total = R.choice([2, 3, 4, 5])
        piece = R.choice([20, 25, 40, 50])
        n = total * 100 // piece
        q = "%s hat ein Band von %s. %s schneidet Stücke von %s ab. Wie viele Stücke bekommt %s?" % (p[0], u(total, "m"), p[1].capitalize(), u(piece, "cm"), p[1])
        return mcq(q, "%d Stücke" % n, ["%d Stücke" % x for x in (n // 2, n + 2, n - 1) if x > 1 and x != n],
                   "%d m = %d cm. %d cm : %d cm = <b>%d</b>." % (total, total * 100, total * 100, piece, n))
    legs = R.randint(3, 5)
    each = R.choice([50, 75, 100, 150, 200])
    q = "Bei einer Staffel laufen %d Kinder je %s. Wie lang ist die ganze Strecke?" % (legs, u(each, "m"))
    r = legs * each
    return mcq(q, u(r, "m"), [u(x, "m") for x in (legs + each, r + each, r - each) if x != r],
               "%d · %d m = <b>%d m</b>." % (legs, each, r))


def main():
    seen = set()
    sets = [
        ("Einheiten umwandeln", mix(R, seen, [(umwandeln, 20)])),
        ("Gemischte Angaben", mix(R, seen, [(gemischt, 20)])),
        ("Am Lineal messen", mix(R, seen, [(messen, 20)])),
        ("Längen vergleichen und rechnen", mix(R, seen, [(vergleichen, 20)])),
        ("Schätzen und Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Längen misst du in Millimeter (mm), Zentimeter (cm), Meter (m) und Kilometer (km).",
         "1 cm = 10 mm, 1 m = 100 cm, 1 km = 1000 m.",
         "Beim Messen legst du das Lineal bei der <b>0</b> an, nicht bei der 1.",
         "Willst du vergleichen oder rechnen, bringe alles in <b>dieselbe Einheit</b>."],
        [example("2 m 5 cm = ? cm", ["2 m = 200 cm", "200 cm + 5 cm = 205 cm"], "205 cm"),
         example("1 m − 35 cm", ["1 m = 100 cm", "100 cm − 35 cm = 65 cm"], "65 cm")],
        [["1 m = 10 cm", "1 m = 100 cm"],
         ["2 m 5 cm = 25 cm", "2 m = 200 cm, also 205 cm"],
         ["Beim Messen bei 1 anfangen", "Immer bei der 0 anlegen"]],
        extra=table(["Einheit", "Umrechnung", "Beispiel"],
                    [["mm", "–", "Ameise"], ["cm", "1 cm = 10 mm", "Fingerbreite"], ["m", "1 m = 100 cm", "großer Schritt"], ["km", "1 km = 1000 m", "Weg zum Nachbarort"]]))
    faq = [
        {"q": "Welche Längeneinheiten lernt man in Klasse 3?", "a": "Millimeter, Zentimeter, Meter und Kilometer, mit den Umrechnungen 1 cm = 10 mm, 1 m = 100 cm und 1 km = 1000 m."},
        {"q": "Wie misst man richtig mit dem Lineal?", "a": "Den Anfang des Gegenstands genau an die 0 legen und am Ende ablesen: erst die ganzen Zentimeter, dann die Millimeter."},
        {"q": "Warum sollen Kinder Längen schätzen?", "a": "Mit Vergleichsgrößen (Fingerbreite ≈ 1 cm, großer Schritt ≈ 1 m) können sie prüfen, ob ein Ergebnis sinnvoll ist."},
        {"q": "Schreibt man in Klasse 3 schon 1,25 m?", "a": "Meist werden Längen in Klasse 3 noch mit zwei Einheiten geschrieben (1 m 25 cm). Die Kommaschreibweise kommt oft in Klasse 4."},
    ]
    make_unit(R, "laengen", "G",
              "Die Schülerinnen und Schüler messen Längen mit dem Lineal, rechnen mit mm, cm, m und km, wandeln Einheiten um und schätzen Längen mit Stützpunktvorstellungen (Zusammenfassung).",
              "Längen: mm, cm, m und km",
              "Längen umrechnen Klasse 3 – mm, cm, m, km Arbeitsblätter mit Lösungen",
              "Längen",
              "Längen für Klasse 3: mm, cm, m und km umrechnen, am Lineal messen, vergleichen, schätzen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen und Arbeitsblatt zum Ausdrucken, kostenlos.",
              "1 cm = 10 mm, 1 m = 100 cm, 1 km = 1000 m",
              "Zum Vergleichen und Rechnen alles in dieselbe Einheit bringen.",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
