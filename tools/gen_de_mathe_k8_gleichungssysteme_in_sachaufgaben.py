# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Gleichungssysteme in Sachaufgaben（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_gleichungssysteme_in_sachaufgaben.py
Passendes Gleichungssystem aufstellen, Zahlenrätsel, Rechtecke, Preise, Eintrittskarten, Köpfe und Beine, Münzen, Mischungen.
Fehler: beide Gleichungen mit derselben Information, Preise den falschen Variablen zugeordnet, Umfang = Länge + Breite, nur eine Größe angegeben.
"""
import random
from de_common import lesson, example, make_unit, mix, MAL, Kids
from de_k6 import dz
from de_k8 import mcq, eur, expr

R = random.Random(49809)
KIDS = Kids(R)


def ansatz():
    kind = R.choice(["zahl", "eintritt", "tiere", "rechteck"])
    if kind == "zahl":
        s, d = R.randint(20, 90), R.randint(2, 18)
        if (s + d) % 2:
            return None
        return mcq("Die Summe zweier Zahlen ist %d, ihre Differenz ist %d. Welches Gleichungssystem passt?" % (s, d), "x + y = %d und x − y = %d" % (s, d),
                   ["x + y = %d und x + y = %d" % (s, d), "x · y = %d und x − y = %d" % (s, d), "x − y = %d und x + y = %d" % (s, d)],
                   "Summe: x + y = %d. Differenz: x − y = %d. <b>x + y = %d und x − y = %d</b>" % (s, d, s, d))
    if kind == "eintritt":
        a, k = R.choice([(8, 5), (12, 6), (10, 4), (9, 6), (15, 8)])
        n, t = R.randint(5, 20), None
        e = R.randint(1, n - 1)
        t = a * e + k * (n - e)
        return mcq("Eine Gruppe von %d Personen zahlt %d € Eintritt. Erwachsene (x) zahlen %d €, Kinder (y) %d €. Welches Gleichungssystem passt?" % (n, t, a, k),
                   "x + y = %d und %dx + %dy = %d" % (n, a, k, t),
                   ["x + y = %d und %dx + %dy = %d" % (t, a, k, n), "x + y = %d und %dx + %dy = %d" % (n, k, a, t), "%dx + %dy = %d und x − y = %d" % (a, k, n, t)],
                   "Personen: x + y = %d. Geld: %dx + %dy = %d. <b>x + y = %d und %dx + %dy = %d</b>" % (n, a, k, t, n, a, k, t))
    if kind == "tiere":
        h, ka = R.randint(3, 15), R.randint(3, 15)
        return mcq("Auf einem Hof leben Hühner (x) und Kaninchen (y). Zusammen haben sie %d Köpfe und %d Beine. Welches Gleichungssystem passt?" % (h + ka, 2 * h + 4 * ka),
                   "x + y = %d und 2x + 4y = %d" % (h + ka, 2 * h + 4 * ka),
                   ["x + y = %d und 4x + 2y = %d" % (h + ka, 2 * h + 4 * ka), "2x + 4y = %d und x + y = %d" % (h + ka, 2 * h + 4 * ka), "x + y = %d und x + y = %d" % (h + ka, 2 * h + 4 * ka)],
                   "Jedes Tier hat einen Kopf: x + y = %d. Hühner 2 Beine, Kaninchen 4: <b>2x + 4y = %d</b>." % (h + ka, 2 * h + 4 * ka))
    b = R.randint(3, 20)
    d = R.randint(2, 10)
    u = 2 * (2 * b + d)
    return mcq("Ein Rechteck hat den Umfang %d cm. Die Länge x ist %d cm größer als die Breite y. Welches Gleichungssystem passt?" % (u, d),
               "2x + 2y = %d und x = y + %d" % (u, d), ["x + y = %d und x = y + %d" % (u, d), "2x + 2y = %d und y = x + %d" % (u, d), "x %s y = %d und x = y + %d" % (MAL, u, d)],
               "Umfang: 2x + 2y = %d. Länge größer: x = y + %d. <b>beide Gleichungen</b>" % (u, d))


def raetsel():
    kind = R.choice(["sumdiff", "vielfach", "rechteck", "alter"])
    if kind == "sumdiff":
        x, y = R.randint(10, 60), R.randint(2, 40)
        if x <= y:
            return None
        return mcq("Die Summe zweier Zahlen ist %d, ihre Differenz ist %d. Wie heißen die Zahlen?" % (x + y, x - y), "%d und %d" % (x, y),
                   ["%d und %d" % (x + 1, y - 1), "%d und %d" % ((x + y) // 2, (x + y) - (x + y) // 2), "%d und %d" % (x + y, x - y)],
                   "I + II: 2x = %d, x = %d. y = %d − %d = %d. <b>%d und %d</b>" % (2 * x, x, x + y, x, y, x, y))
    if kind == "vielfach":
        y = R.randint(3, 20)
        k = R.choice([2, 3, 4, 5])
        x = k * y
        return mcq("Eine Zahl ist %d-mal so groß wie eine andere. Zusammen ergeben sie %d. Wie heißen die Zahlen?" % (k, x + y), "%d und %d" % (x, y),
                   ["%d und %d" % ((x + y) // 2, (x + y) - (x + y) // 2), "%d und %d" % ((x + y) - (x + y) // k, (x + y) // k) if (x + y) % k == 0 and (x + y) // k != y else "%d und %d" % (x - 1, y + 1), "%d und %d" % (x + y - k, k)],
                   "x = %dy einsetzen: %dy + y = %d, also %dy = %d, y = %d und x = %d. <b>%d und %d</b>" % (k, k, x + y, k + 1, x + y, y, x, x, y))
    if kind == "rechteck":
        b = R.randint(3, 20)
        d = R.randint(2, 10)
        l = b + d
        return mcq("Ein Rechteck hat den Umfang %d cm. Die Länge ist %d cm größer als die Breite. Wie lang sind die Seiten?" % (2 * (l + b), d), "Länge %d cm, Breite %d cm" % (l, b),
                   ["Länge %d cm, Breite %d cm" % ((2 * (l + b) + d) // 2, (2 * (l + b) - d) // 2) if d % 2 == 0 else "Länge %d cm, Breite %d cm" % (l + 1, b + 1),
                    "Länge %d cm, Breite %d cm" % (l + d, b + d), "Länge %d cm, Breite %d cm" % (b, l)],
                   "x + y = %d (halber Umfang), x − y = %d. 2x = %d, x = %d, y = %d. <b>Länge %d cm, Breite %d cm</b>" % (l + b, d, 2 * l, l, b, l, b))
    k = R.choice([3, 4])
    c = R.randint(8, 13)
    m = k * c
    if m < 30 or m > 50:
        return None
    return mcq("Eine Mutter ist %d-mal so alt wie ihr Kind. Zusammen sind sie %d Jahre alt. Wie alt sind beide?" % (k, m + c), "Mutter %d, Kind %d" % (m, c),
               ["Mutter %d, Kind %d" % ((m + c) // 2 + 5, (m + c) - (m + c) // 2 - 5), "Mutter %d, Kind %d" % (m + c - k, k), "Mutter %d, Kind %d" % (m - c, c + c)],
               "x = %dy, x + y = %d: %dy = %d, y = %d, x = %d. <b>Mutter %d, Kind %d</b>" % (k, m + c, k + 1, m + c, c, m, m, c))


PREIS = [("Hefte", "Stifte", (120, 250), (60, 150)), ("Brötchen", "Brezeln", (40, 70), (70, 110)), ("Kugeln Eis", "Waffeln", (120, 180), (30, 80)),
         ("Äpfel", "Birnen", (30, 60), (40, 80)), ("Cola", "Wasser", (150, 250), (80, 140)), ("Postkarten", "Briefmarken", (100, 180), (80, 130))]


def preise():
    a, b, ra, rb = R.choice(PREIS)
    pa, pb = R.randrange(ra[0], ra[1], 10), R.randrange(rb[0], rb[1], 10)
    if pa == pb:
        return None
    m1, n1 = R.randint(1, 4), R.randint(1, 4)
    m2, n2 = R.randint(1, 4), R.randint(1, 4)
    if m1 * n2 == m2 * n1:
        return None
    t1, t2 = m1 * pa + n1 * pb, m2 * pa + n2 * pb
    ask = R.choice([0, 1])
    q = "%d %s und %d %s kosten %s. %d %s und %d %s kosten %s. Was kostet %s?" % (m1, a, n1, b, eur(t1 / 100), m2, a, n2, b, eur(t2 / 100), (["ein Heft", "ein Brötchen", "eine Kugel Eis", "ein Apfel", "eine Cola", "eine Postkarte"][[p[0] for p in PREIS].index(a)]) if ask == 0 else ["ein Stift", "eine Brezel", "eine Waffel", "eine Birne", "ein Wasser", "eine Briefmarke"][[p[0] for p in PREIS].index(a)])
    ans = eur((pa if ask == 0 else pb) / 100)
    return mcq(q.replace("1 Hefte", "1 Heft").replace("1 Stifte", "1 Stift").replace("1 Brötchen", "1 Brötchen").replace("1 Brezeln", "1 Brezel").replace("1 Kugeln Eis", "1 Kugel Eis").replace("1 Waffeln", "1 Waffel").replace("1 Äpfel", "1 Apfel").replace("1 Birnen", "1 Birne").replace("1 Postkarten", "1 Postkarte").replace("1 Briefmarken", "1 Briefmarke"),
               ans, [eur((pb if ask == 0 else pa) / 100), eur(t1 / 100 / (m1 + n1)), eur(abs(t1 - t2) / 100)],
               "x = Preis für %s, y = Preis für %s (in Cent). I: %s = %d, II: %s = %d. Lösung: x = %d, y = %d. <b>%s</b>" % (["ein Heft", "ein Brötchen", "eine Kugel Eis", "einen Apfel", "eine Cola", "eine Postkarte"][[p[0] for p in PREIS].index(a)], ["einen Stift", "eine Brezel", "eine Waffel", "eine Birne", "ein Wasser", "eine Briefmarke"][[p[0] for p in PREIS].index(a)], expr([(m1, "x"), (n1, "y")]), t1, expr([(m2, "x"), (n2, "y")]), t2, pa, pb, ans))


def anzahl():
    kind = R.choice(["eintritt", "tiere", "muenzen", "tische"])
    if kind == "eintritt":
        a, k = R.choice([(8, 5), (12, 6), (10, 4), (9, 6), (15, 8)])
        n = R.randint(6, 25)
        e = R.randint(1, n - 1)
        t = a * e + k * (n - e)
        return mcq("Ein Museum: Erwachsene zahlen %d €, Kinder %d €. Eine Gruppe aus %d Personen zahlt %d €. Wie viele Kinder sind dabei?" % (a, k, n, t), "%d Kinder" % (n - e),
                   ["%d Kinder" % e, "%d Kinder" % (t // (a + k)) if t // (a + k) not in (e, n - e) else "%d Kinder" % (n - e + 1), "%d Kinder" % (n // 2) if n // 2 not in (e, n - e) else "%d Kinder" % (n - e - 1)],
                   "x + y = %d, %dx + %dy = %d. Mit x = %d − y: %d(%d − y) + %dy = %d, also y = %d. <b>%d Kinder</b> (und %d Erwachsene)" % (n, a, k, t, n, a, n, k, t, n - e, n - e, e))
    if kind == "tiere":
        h, ka = R.randint(3, 20), R.randint(3, 20)
        return mcq("Auf einem Hof gibt es Hühner und Kaninchen, zusammen %d Köpfe und %d Beine. Wie viele Kaninchen sind es?" % (h + ka, 2 * h + 4 * ka), "%d Kaninchen" % ka,
                   ["%d Kaninchen" % h if h != ka else "%d Kaninchen" % (ka + 1), "%d Kaninchen" % ((2 * h + 4 * ka) // 4), "%d Kaninchen" % ((h + ka) // 2) if (h + ka) // 2 not in (h, ka) else "%d Kaninchen" % (ka + 2)],
                   "x + y = %d, 2x + 4y = %d. I mal 2 abziehen: 2y = %d, <b>y = %d Kaninchen</b>." % (h + ka, 2 * h + 4 * ka, 2 * ka, ka))
    if kind == "muenzen":
        z, e = R.randint(2, 15), R.randint(2, 15)
        name, er = KIDS.next()
        return mcq("%s hat %d Münzen, nur 1-€- und 2-€-Münzen, zusammen %d €. Wie viele 2-€-Münzen sind es?" % (name, z + e, 2 * z + e), "%d" % z,
                   ["%d" % e if e != z else "%d" % (z + 1), "%d" % ((2 * z + e) // 2), "%d" % (2 * z + e - (z + e) - 1) if (2 * z + e - (z + e) - 1) not in (z, e) else "%d" % (z + 2)],
                   "x + y = %d, 2x + y = %d. II − I: <b>x = %d</b> Zwei-Euro-Münzen." % (z + e, 2 * z + e, z))
    v, s = R.randint(3, 12), R.randint(3, 12)
    return mcq("In einem Café gibt es Vierertische und Sechsertische, zusammen %d Tische mit %d Plätzen. Wie viele Sechsertische gibt es?" % (v + s, 4 * v + 6 * s), "%d" % s,
               ["%d" % v if v != s else "%d" % (s + 1), "%d" % ((4 * v + 6 * s) // 10), "%d" % ((v + s) // 2) if (v + s) // 2 not in (v, s) else "%d" % (s + 2)],
               "x + y = %d, 4x + 6y = %d. I mal 4 abziehen: 2y = %d, <b>y = %d</b>." % (v + s, 4 * v + 6 * s, 2 * s, s))


def gemischt():
    return R.choice([raetsel, preise, anzahl])()


def main():
    seen = set()
    sets = [
        ("Gleichungssystem aufstellen", mix(R, seen, [(ansatz, 20)])),
        ("Zahlenrätsel und Figuren", mix(R, seen, [(raetsel, 20)])),
        ("Preise", mix(R, seen, [(preise, 20)])),
        ("Anzahlen bestimmen", mix(R, seen, [(anzahl, 20)])),
        ("Gemischte Sachaufgaben", mix(R, seen, [(gemischt, 20)])),
    ]
    body = lesson(
        ["1. Die beiden Unbekannten festlegen: „x = Anzahl der Erwachsenen, y = Anzahl der Kinder“.",
         "2. Für jede Information eine Gleichung aufstellen. Zwei verschiedene Informationen ergeben zwei Gleichungen.",
         "3. Das Gleichungssystem lösen (gleichsetzen, einsetzen oder addieren).",
         "4. Die Lösung am Text prüfen und einen Antwortsatz schreiben."],
        [example("Hühner und Kaninchen: 10 Köpfe, 28 Beine", ["x + y = 10", "2x + 4y = 28", "2y = 8, y = 4"], "6 Hühner, 4 Kaninchen"),
         example("2 Hefte und 1 Stift kosten 4 €, 1 Heft und 2 Stifte kosten 3,50 €", ["2x + y = 4, x + 2y = 3,5", "x = 1,50, y = 1"], "Heft 1,50 €, Stift 1 €")],
        [["Umfang 30: x + y = 30", "2x + 2y = 30"],
         ["Köpfe und Beine: x + y = 28 und 2x + 4y = 10", "Köpfe zur Anzahl, Beine zu 2x + 4y"],
         ["Nur x angeben", "Nach beiden Größen fragen und antworten"]])
    faq = [
        {"q": "Wie stelle ich ein Gleichungssystem aus einem Text auf?", "a": "Lege zwei Variablen fest und übersetze jede der beiden Informationen in eine Gleichung."},
        {"q": "Welches Verfahren nehme ich bei Sachaufgaben?", "a": "Steht eine Gleichung wie x = 3y schon aufgelöst da, ist Einsetzen günstig. Bei x + y und 2x + 4y hilft das Additionsverfahren."},
        {"q": "Wie prüfe ich das Ergebnis?", "a": "Setze die Zahlen in den Text ein: Stimmen Anzahl und Summe (Preis, Beine, Umfang)? Dann ist die Lösung richtig."},
        {"q": "Warum brauche ich zwei Gleichungen?", "a": "Mit zwei Unbekannten braucht man zwei unabhängige Informationen, sonst gibt es viele Lösungen."},
    ]
    make_unit(R, "gleichungssysteme-in-sachaufgaben", "F",
              "Die Schülerinnen und Schüler übersetzen Sachsituationen in lineare Gleichungssysteme mit zwei Variablen, lösen sie und prüfen die Ergebnisse am Sachkontext (Zusammenfassung).",
              "Gleichungssysteme in Sachaufgaben",
              "Lineare Gleichungssysteme Textaufgaben Klasse 8 – mit Lösungen",
              "LGS Textaufgaben",
              "Textaufgaben zu linearen Gleichungssystemen für Klasse 8: aufstellen, Zahlenrätsel, Rechtecke, Preise, Eintrittskarten, Köpfe und Beine. 100 Aufgaben mit Lösungen, kostenlos.",
              "Zwei Unbekannte, zwei Gleichungen.",
              "Variablen festlegen, Gleichungen aufstellen, lösen, prüfen.",
              body, faq, sets, 9, grade="klasse-8")


if __name__ == "__main__":
    main()
