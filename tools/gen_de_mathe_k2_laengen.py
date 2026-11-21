# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Längen – Zentimeter und Meter（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k2_laengen.py
Am Lineal messen, cm und m umwandeln, Längen vergleichen, mit Längen rechnen, schätzen und Sachaufgaben.
Fehler: am Lineal bei 1 statt bei 0 anfangen, 1 m = 10 cm, Längen mit verschiedenen Einheiten direkt verglichen.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, table
from gen_de_mathe_k3_laengen import lineal

R = random.Random(49213)
KIDS = Kids(R)


def m_cm(cm):
    m, c = divmod(cm, 100)
    if m and c:
        return "%d m %d cm" % (m, c)
    return "%d m" % m if m else "%d cm" % c


def messen():
    start = R.choice([0, 0, 0, 10, 20, 30, 10])
    L = R.randint(2, 11 - start // 10) * 10
    pic = lineal(start, L, cm=12)
    c = L // 10
    w = [c + start // 10, c + 1, c - 1]
    if start == 0:
        w[0] = c + 2
    return mcq(pic + "Wie lang ist der Streifen?", "%d cm" % c, ["%d cm" % x for x in w if x > 0 and x != c],
               ("Der Streifen beginnt bei 0 und endet bei %d: <b>%d cm</b>." % (c, c)) if start == 0 else
               "Der Streifen beginnt bei %d und endet bei %d: %d − %d = <b>%d cm</b>." % (start // 10, start // 10 + c, start // 10 + c, start // 10, c))


def umwandeln():
    kind = R.choice(["m_zu_cm", "cm_zu_m", "gemischt", "gemischt_zu_cm"])
    if kind == "m_zu_cm":
        a = R.randint(1, 9)
        return mcq("%d m = ? cm" % a, "%d cm" % (100 * a), ["%d cm" % x for x in (10 * a, a, 1000 * a)],
                   "1 m = 100 cm. %d m = <b>%d cm</b>." % (a, 100 * a))
    if kind == "cm_zu_m":
        a = R.randint(1, 9)
        return mcq("%d cm = ? m" % (100 * a), "%d m" % a, ["%d m" % x for x in (10 * a, 100 * a, a + 1)],
                   "100 cm = 1 m. %d cm = <b>%d m</b>." % (100 * a, a))
    a, c = R.randint(1, 4), R.randint(5, 95)
    tot = 100 * a + c
    if kind == "gemischt":
        return mcq("%d cm = ?" % tot, m_cm(tot), ["%d m %d cm" % (tot // 10, tot % 10), "%d m %d cm" % (a + 1, c), "%d m %d cm" % (c, a) if c < 100 else "%d m" % a],
                   "100 cm sind 1 m. %d cm = <b>%s</b>." % (tot, m_cm(tot)))
    return mcq("%d m %d cm = ? cm" % (a, c), "%d cm" % tot, ["%d cm" % x for x in (10 * a + c, a + c, 100 * a + c * 10 if c < 10 else 100 * (a + 1) + c)],
               "%d m = %d cm, dazu %d cm: <b>%d cm</b>." % (a, 100 * a, c, tot))


def vergleichen():
    kind = R.choice(["zwei", "ordnen", "kind"])
    if kind == "zwei":
        a = R.randint(1, 3)
        b = R.choice([a * 100 + R.randint(-60, 60), a * 10, a * 100 - R.randint(1, 30)])
        if b <= 0 or b == a * 100:
            return None
        big = "%d m" % a if a * 100 > b else "%d cm" % b
        return mcq("Was ist länger: %d m oder %d cm?" % (a, b), big, ["%d cm" % b if big.endswith(" m") else "%d m" % a, "Beide sind gleich lang", "Das kann man nicht vergleichen"],
                   "%d m = %d cm. Länger ist <b>%s</b>." % (a, 100 * a, big))
    if kind == "ordnen":
        vals = R.sample(range(60, 260, 5), 3)
        txt = [m_cm(v) if R.random() < 0.6 else "%d cm" % v for v in vals]
        k = vals.index(max(vals))
        return mcq("Welche Länge ist am größten? %s" % ", ".join(txt), txt[k], [t for i, t in enumerate(txt) if i != k] + ["Alle sind gleich lang"],
                   "In Zentimetern: %s. Am größten ist <b>%s</b>." % (", ".join("%d cm" % v for v in vals), txt[k]))
    (n1, _), (n2, _) = KIDS.two()
    a, b = R.randint(115, 140), R.randint(115, 140)
    if a == b:
        return None
    big = n1 if a > b else n2
    return mcq("%s ist %s groß, %s ist %d cm groß. Wer ist größer?" % (n1, m_cm(a), n2, b), big, [n2 if big == n1 else n1, "Beide sind gleich groß", "Das kann man nicht sagen"],
               "%s = %d cm. %s ist größer: <b>%s</b>." % (m_cm(a), a, big, big))


def rechnen():
    kind = R.choice(["plus", "minus", "fehlt", "mal"])
    if kind == "plus":
        a, b = R.randint(15, 60), R.randint(12, 39)
        return mcq("%d cm + %d cm = ?" % (a, b), "%d cm" % (a + b), ["%d cm" % x for x in (a + b + 10, a - b if a > b else a + b - 1, a + b - 10)],
                   "%d + %d = <b>%d cm</b>." % (a, b, a + b))
    if kind == "minus":
        a = R.randint(2, 9)
        b = R.randint(10, 90)
        return mcq("%d m − %d cm = ?" % (a, b), m_cm(100 * a - b), [m_cm(100 * a - b + 100), "%d m" % (a - 1), m_cm(abs(10 * a - b) or 1)],
                   "%d m = %d cm. %d − %d = %d cm = <b>%s</b>." % (a, 100 * a, 100 * a, b, 100 * a - b, m_cm(100 * a - b)))
    if kind == "fehlt":
        a = R.randint(12, 95)
        return mcq("%d cm + ? = 1 m" % a, "%d cm" % (100 - a), ["%d cm" % x for x in (100 - a + 10, 100 - a - 1, (10 - a // 10) * 10 + (10 - a % 10) if a % 10 else 100 - a + 20)],
                   "1 m = 100 cm. %d + %d = 100: <b>%d cm</b>." % (a, 100 - a, 100 - a))
    k, c = R.randint(2, 5), R.randint(5, 20)
    return mcq("%d Bausteine liegen hintereinander. Jeder ist %d cm lang. Wie lang ist die Reihe?" % (k, c), "%d cm" % (k * c), ["%d cm" % x for x in (k + c, k * c + c, k * c - c)],
               "%d · %d cm = <b>%d cm</b>." % (k, c, k * c))


SCHAETZ = [("Wie lang ist ein Bleistift ungefähr?", "17 cm", ["17 m", "1 cm", "170 cm"]),
           ("Wie hoch ist eine Tür ungefähr?", "2 m", ["2 cm", "20 m", "20 cm"]),
           ("Wie lang ist ein Schulheft ungefähr?", "30 cm", ["30 m", "3 cm", "3 m"]),
           ("Wie groß ist ein Kind in Klasse 2 ungefähr?", "1 m 25 cm", ["25 cm", "12 m", "2 m 50 cm"]),
           ("Wie lang ist ein Klassenzimmer ungefähr?", "8 m", ["8 cm", "80 cm", "80 m"]),
           ("Wie breit ist ein Daumen ungefähr?", "2 cm", ["2 m", "20 cm", "20 m"]),
           ("Wie lang ist ein Linienbus ungefähr?", "12 m", ["12 cm", "120 m", "1 m"]),
           ("Wie hoch ist ein Tisch ungefähr?", "75 cm", ["75 m", "7 cm", "7 m"]),
           ("Wie lang ist ein Turnschuh ungefähr?", "20 cm", ["2 m", "2 cm", "20 m"]),
           ("Wie lang ist ein Löffel ungefähr?", "15 cm", ["15 m", "1 cm", "150 cm"])]


def sache():
    kind = R.choice(["schaetz", "schaetz", "sprung", "band", "weg"])
    p = KIDS.next()
    if kind == "schaetz":
        q, a, w = R.choice(SCHAETZ)
        return mcq(q, a, w, "Stell dir den Gegenstand vor und vergleiche mit 1 cm (Fingerbreite) und 1 m (ein großer Schritt): <b>%s</b>." % a)
    if kind == "sprung":
        a, b = R.randint(150, 260), R.randint(150, 260)
        if a == b:
            return None
        (n1, _), (n2, _) = KIDS.two()
        d = abs(a - b)
        win = n1 if a > b else n2
        return mcq("Beim Weitsprung springt %s %s und %s %s. Wie viel weiter springt %s?" % (n1, m_cm(a), n2, m_cm(b), win), "%d cm" % d,
                   ["%d cm" % x for x in (a + b, d + 10, d + 100)], "%d cm − %d cm = <b>%d cm</b>." % (max(a, b), min(a, b), d))
    if kind == "band":
        a = R.randint(1, 3)
        b = R.randint(20, 80)
        return mcq("%s hat ein Band, das %d m lang ist. %s schneidet %d cm ab. Wie lang ist das Band jetzt?" % (p[0], a, p[1].capitalize(), b), m_cm(100 * a - b),
                   [m_cm(100 * a + b), m_cm(100 * a - b + 10), "%d cm" % (abs(10 * a - b) or 5)],
                   "%d m = %d cm. %d − %d = %d cm = <b>%s</b>." % (a, 100 * a, 100 * a, b, 100 * a - b, m_cm(100 * a - b)))
    a, b = R.randint(12, 48) * 10, R.randint(12, 48) * 10
    if a + b > 1000 or a == b:
        return None
    return mcq("Der Weg von %s zur Schule ist %d m lang, der Weg zurück über den Spielplatz %d m. Wie viele Meter läuft %s an diesem Tag?" % (p[0], a, b, p[1]), "%d m" % (a + b),
               ["%d m" % x for x in (abs(a - b), a + b + 100, a + b - 10)], "%d m + %d m = <b>%d m</b>." % (a, b, a + b))


def main():
    seen = set()
    sets = [
        ("Am Lineal messen", mix(R, seen, [(messen, 20)])),
        ("Zentimeter und Meter", mix(R, seen, [(umwandeln, 20)])),
        ("Längen vergleichen", mix(R, seen, [(vergleichen, 20)])),
        ("Mit Längen rechnen", mix(R, seen, [(rechnen, 20)])),
        ("Schätzen und Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Kurze Längen misst du in <b>Zentimetern</b> (cm), lange Längen in <b>Metern</b> (m).",
         "<b>1 m = 100 cm</b>. 1 m 25 cm sind 125 cm.",
         "Beim Messen legst du das Lineal bei der <b>0</b> an, nicht bei der 1.",
         "Willst du Längen vergleichen, schreibe sie erst in derselben Einheit."],
        [example("Ein Streifen geht von 2 bis 9 am Lineal", ["9 − 2 = 7"], "7 cm"),
         example("Was ist länger: 1 m oder 90 cm?", ["1 m = 100 cm", "100 cm &gt; 90 cm"], "1 m")],
        [["Am Lineal bei 1 anfangen", "Immer bei 0 anfangen"],
         ["1 m = 10 cm", "1 m = 100 cm"],
         ["90 cm ist länger als 1 m, weil 90 größer ist", "Erst umwandeln: 1 m = 100 cm"]],
        extra=table(["Gegenstand", "ungefähre Länge"], [["Fingerbreite", "1 cm"], ["Bleistift", "17 cm"], ["großer Schritt", "1 m"], ["Tür", "2 m"]]))
    faq = [
        {"q": "Welche Längeneinheiten lernen Kinder in Klasse 2?", "a": "Zentimeter und Meter. Millimeter und Kilometer kommen in Klasse 3 dazu."},
        {"q": "Warum ist Schätzen wichtig?", "a": "Wer weiß, wie lang 1 cm und 1 m ungefähr sind, erkennt falsche Ergebnisse. Ein Bleistift ist nicht 17 m lang."},
        {"q": "Wie misst man richtig mit dem Lineal?", "a": "Das Lineal wird genau bei der 0 angelegt. Dann liest man ab, wo der Gegenstand endet."},
        {"q": "Wie schreibt man 135 cm?", "a": "Als 1 m 35 cm. Die Kommaschreibweise 1,35 m lernen die Kinder meist erst in Klasse 3 oder 4."},
    ]
    make_unit(R, "laengen", "G",
              "Die Schülerinnen und Schüler messen Längen mit dem Lineal, wandeln Zentimeter und Meter um, vergleichen und schätzen Längen und rechnen mit Längen in Sachsituationen (Zusammenfassung).",
              "Längen: Zentimeter und Meter",
              "Längen messen Klasse 2 – Arbeitsblätter mit Lösungen",
              "Längen",
              "Längen für Klasse 2: am Lineal messen, Zentimeter und Meter umwandeln, vergleichen, rechnen und schätzen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 m = 100 cm",
              "Am Lineal immer bei 0 anfangen.",
              body, faq, sets, 13, grade="klasse-2")


if __name__ == "__main__":
    main()
