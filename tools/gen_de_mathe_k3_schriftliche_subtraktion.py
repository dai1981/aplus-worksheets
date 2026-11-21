# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Schriftliche Subtraktion（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_schriftliche_subtraktion.py
Ohne Entbündeln, mit einmal und zweimal Entbündeln, mit Nullen, Probe, fehlende Ziffern, Sachaufgaben.
Fehler: kleine Ziffer von großer abziehen (632 − 257 → 425), entbündelt aber nicht verringert (→ 485), Fehler bei Nullen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, schriftlich, Kids

R = random.Random(49006)
KIDS = Kids(R)


def cols(n):
    return [int(d) for d in str(n).rjust(3, "0")][::-1]


def borrows(a, b):
    n, c = 0, 0
    for k in range(3):
        if cols(a)[k] - c < cols(b)[k]:
            n += 1
            c = 1
        else:
            c = 0
    return n


def small_big(a, b):
    return int("".join(str(abs(cols(a)[k] - cols(b)[k])) for k in (2, 1, 0)))


def no_reduce(a, b):
    """entbündelt (10 dazu), aber die nächste Stelle nicht verringert"""
    out = []
    for k in range(3):
        x, y = cols(a)[k], cols(b)[k]
        out.append((x + 10 - y) % 10 if x < y else x - y)
    return int("".join(str(d) for d in out[::-1]))


def task(a, b, need, zero=False):
    if a - b < 1 or borrows(a, b) != need:
        return None
    if zero and "0" not in str(a)[1:]:
        return None
    r = a - b
    w = [small_big(a, b), no_reduce(a, b), r + 10, r - 10, r + 100, r + 1]
    pic = schriftlich([str(a), str(b)], op="−")
    e = "Von rechts nach links. %sErgebnis: <b>%s</b>. Probe: %s + %s = %s." % (
        "Reicht eine Ziffer nicht, entbündelst du: 1 Zehner = 10 Einer (oder 1 Hunderter = 10 Zehner). " if need else "",
        num(r), num(r), num(b), num(a))
    return mcq(pic + "Rechne schriftlich: %s − %s" % (num(a), num(b)), num(r),
               [num(x) for x in w if x > 0 and x != r and x < 1000], e)


def s1():
    a = R.randint(350, 999)
    b = R.randint(110, a - 100)
    return task(a, b, 0)


def s2():
    a = R.randint(320, 999)
    b = R.randint(110, a - 60)
    return task(a, b, 1)


def s3():
    a = R.randint(400, 999)
    b = R.randint(120, a - 40)
    return task(a, b, 2)


def s4_null():
    a = R.choice([R.randint(3, 9) * 100 + R.randint(1, 9), R.randint(3, 9) * 100 + R.randint(1, 9) * 10, R.randint(3, 9) * 100])
    b = R.randint(111, a - 50)
    n = borrows(a, b)
    if n == 0:
        return None
    return task(a, b, n, zero=True)


def s4_probe():
    a = R.randint(400, 950)
    b = R.randint(120, a - 80)
    r = a - b
    claim = R.choice([r, r + 10, r - 10, small_big(a, b) if small_big(a, b) != r else r + 100])
    ok = claim == r
    q = "Paula rechnet %s − %s = %s. Welche Probe zeigt, ob das stimmt?" % (num(a), num(b), num(claim))
    s = claim + b
    ans = "%s + %s = %s, also %s" % (num(claim), num(b), num(s), "richtig" if ok else "falsch")
    w = ["%s + %s = %s, also %s" % (num(claim), num(b), num(s), "falsch" if ok else "richtig"),
         "%s + %s = %s, also richtig" % (num(a), num(b), num(a + b)),
         "%s − %s = %s, also %s" % (num(a), num(claim), num(a - claim), "falsch" if ok else "richtig")]
    return mcq(q, ans, w, "Probe mit der Plusaufgabe: Ergebnis + abgezogene Zahl muss die erste Zahl ergeben. %s + %s = %s, also <b>%s</b>."
               % (num(claim), num(b), num(s), "richtig" if ok else "falsch"))


def s4_luecke():
    a = R.randint(400, 950)
    b = R.randint(120, a - 80)
    r = a - b
    k = R.choice([1, 2])
    s = str(r).rjust(3, "0")
    if s[0] == "0":
        return None
    d = int(s[k])
    shown = s[:k] + "☐" + s[k + 1:]
    q = "Welche Ziffer fehlt im Ergebnis? %s − %s = %s" % (num(a), num(b), shown)
    w = [(d + 1) % 10, (d - 1) % 10, int(str(small_big(a, b)).rjust(3, "0")[k]), (d + 2) % 10]
    return mcq(q, str(d), [str(x) for x in w if x != d],
               "%s − %s = %s. Die fehlende Ziffer ist <b>%d</b>." % (num(a), num(b), num(r), d))


def s5_sache():
    kind = R.choice(["buch", "geld", "weg", "baum", "konzert"])
    p = KIDS.next()
    if kind == "buch":
        a = R.randint(220, 480)
        b = R.randint(70, a - 40)
        q = "Ein Buch hat %s Seiten. %s hat schon %s Seiten gelesen. Wie viele Seiten muss %s noch lesen?" % (num(a), p[0], num(b), p[1])
        u = "Seiten"
    elif kind == "geld":
        a = R.randint(300, 900)
        b = R.randint(120, a - 50)
        q = "%s hat %s € gespart und kauft ein Fahrrad für %s €. Wie viel Geld bleibt übrig?" % (p[0], num(a), num(b))
        u = "€"
    elif kind == "weg":
        a = R.randint(400, 900)
        b = R.randint(150, a - 60)
        q = "Familie Becker fährt %s km in den Urlaub. Nach der Pause sind schon %s km geschafft. Wie viele Kilometer fehlen noch?" % (num(a), num(b))
        u = "km"
    elif kind == "baum":
        a = R.randint(400, 999)
        b = R.randint(150, a - 60)
        q = "Ein Bauer hat %s Apfelbäume. %s Bäume sind schon abgeerntet. Wie viele Bäume muss er noch ernten?" % (num(a), num(b))
        u = "Bäume"
    else:
        a = R.randint(400, 800)
        b = R.randint(150, a - 60)
        q = "In der Halle gibt es %s Plätze. %s Karten sind verkauft. Wie viele Plätze sind noch frei?" % (num(a), num(b))
        u = "Plätze"
    if borrows(a, b) == 0:
        return None
    r = a - b
    w = [small_big(a, b), no_reduce(a, b), a + b if a + b <= 1000 else r + 100, r + 10]
    return mcq(q, "%s %s" % (num(r), u), ["%s %s" % (num(x), u) for x in w if x > 0 and x != r],
               "%s − %s = <b>%s %s</b>. Probe: %s + %s = %s." % (num(a), num(b), num(r), u, num(r), num(b), num(a)))


def main():
    seen = set()
    sets = [
        ("Ohne Entbündeln", mix(R, seen, [(s1, 20)])),
        ("Einmal entbündeln", mix(R, seen, [(s2, 20)])),
        ("Zweimal entbündeln", mix(R, seen, [(s3, 20)])),
        ("Nullen, Probe und fehlende Ziffern", mix(R, seen, [(s4_null, 10), (s4_probe, 5), (s4_luecke, 5)])),
        ("Sachaufgaben", mix(R, seen, [(s5_sache, 20)])),
    ]
    body = lesson(
        ["Schreibe die Zahlen genau untereinander. Rechne von <b>rechts nach links</b>.",
         "Ist die obere Ziffer zu klein, <b>entbündelst</b> du: Du nimmst einen Zehner weg und hast 10 Einer mehr (oder einen Hunderter für 10 Zehner).",
         "Die Ziffer, von der du entbündelt hast, wird um 1 kleiner. Streiche sie durch und schreibe die neue Ziffer darüber.",
         "Mache die <b>Probe</b> mit Plus: Ergebnis + untere Zahl = obere Zahl."],
        [example("632 − 257",
                 ["Einer: 2 − 7 geht nicht → 1 Zehner entbündeln: 12 − 7 = 5", "Zehner: noch 2, 2 − 5 geht nicht → 1 Hunderter entbündeln: 12 − 5 = 7",
                  "Hunderter: noch 5, 5 − 2 = 3", "Probe: 375 + 257 = 632"], "375"),
         example("503 − 128", ["Einer: 3 − 8 geht nicht, bei den Zehnern ist 0 → erst 1 Hunderter in 10 Zehner, dann 1 Zehner in 10 Einer",
                               "13 − 8 = 5, 9 − 2 = 7, 4 − 1 = 3"], "375")],
        [["632 − 257 = 425 (kleine von großer Ziffer)", "Oben minus unten! Reicht es nicht, entbündeln: 375"],
         ["Entbündelt, aber die Ziffer links nicht verkleinert: 485", "Die Ziffer links wird um 1 kleiner: 375"],
         ["Bei 503 − 128 die 0 vergessen", "Über die 0 hinweg entbündeln: aus 5 H 0 Z wird 4 H 10 Z"]])
    faq = [
        {"q": "Welches Verfahren lernen die Kinder?", "a": "Das hängt vom Bundesland und vom Schulbuch ab. Oft wird das Abziehverfahren mit Entbündeln gelernt, manche Schulen nutzen das Ergänzungsverfahren. Das Ergebnis ist bei beiden gleich."},
        {"q": "Was heißt entbündeln?", "a": "Einen Zehner in 10 Einer (oder einen Hunderter in 10 Zehner) umtauschen, damit die Subtraktion in einer Spalte möglich wird."},
        {"q": "Warum sind Nullen schwierig?", "a": "Bei 503 − 128 kann man bei den Zehnern nichts entbündeln. Man muss erst einen Hunderter in 10 Zehner tauschen."},
        {"q": "Wie macht man die Probe?", "a": "Man addiert das Ergebnis und die abgezogene Zahl. Kommt die erste Zahl heraus, stimmt die Rechnung."},
    ]
    make_unit(R, "schriftliche-subtraktion", "Z",
              "Die Schülerinnen und Schüler führen die schriftliche Subtraktion im Zahlenraum bis 1000 aus, verstehen das Entbündeln (bzw. Ergänzen mit Übertrag) und kontrollieren mit der Probe (Zusammenfassung).",
              "Schriftliche Subtraktion mit Entbündeln",
              "Schriftliche Subtraktion Klasse 3 – Arbeitsblätter mit Lösungen",
              "Schriftliche Subtraktion",
              "Schriftliche Subtraktion für Klasse 3: ohne und mit Entbündeln, Aufgaben mit Nullen, Probe und Sachaufgaben. 100 Übungsaufgaben mit Lösungen und Arbeitsblatt zum Ausdrucken, kostenlos.",
              "Oben minus unten, von rechts nach links.",
              "Reicht eine Ziffer nicht, entbündelst du von der nächsten Stelle.",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
