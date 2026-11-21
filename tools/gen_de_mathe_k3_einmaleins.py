# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Das kleine Einmaleins（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_einmaleins.py
Kernaufgaben (2, 5, 10), schwierige Reihen (6, 7, 8, 9), Geteiltaufgaben, Platzhalter und Aufgabenfamilien, Sachaufgaben.
Fehler: Nachbaraufgabe (7 · 8 → 49 oder 63), plus statt mal (7 · 8 → 15), Ergebnis der falschen Reihe.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, wrap, MAL, GETEILT
from ws_common import text, INK, GREEN, FILL

R = random.Random(49007)
KIDS = Kids(R)


def punkte(rows, cols):
    s = []
    for r in range(rows):
        for c in range(cols):
            s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='1.3'/>" % (14 + c * 20 + (c // 5) * 6, 14 + r * 20 + (r // 5) * 6, FILL, GREEN))
    return wrap(28 + cols * 20 + (cols // 5) * 6, 28 + rows * 20 + (rows // 5) * 6, "".join(s), "Punktefeld mit %d Reihen zu je %d" % (rows, cols))


def wrongs_mul(a, b):
    r = a * b
    return [a * (b + 1), a * (b - 1) if b > 1 else a * (b + 2), (a + 1) * b, a + b, r + 1, r - 1, r + 10]


def mul(lo_set):
    def mk():
        a = R.choice(lo_set)
        b = R.randint(2, 10)
        if R.random() < 0.5:
            a, b = b, a
        r = a * b
        pic = punkte(a, b) if a <= 6 and b <= 10 and R.random() < 0.35 else ""
        return mcq(pic + "%d %s %d = ?" % (a, MAL, b), num(r), [num(x) for x in wrongs_mul(a, b) if x > 0 and x != r],
                   "%d %s %d bedeutet %d-mal die %d. Ergebnis: <b>%d</b>." % (a, MAL, b, a, b, r))
    return mk


def nachbar():
    a = R.choice([6, 7, 8, 9])
    b = R.choice([6, 7, 8, 9])
    k = R.choice([5, 10])
    if b == k:
        return None
    r = a * b
    q = "Du weißt: %d %s %d = %d. Wie viel ist %d %s %d?" % (a, MAL, k, a * k, a, MAL, b)
    w = [a * k + (b - k) if k < b else a * k - (k - b), a * (b + 1), a * (b - 1), r + a]
    return mcq(q, num(r), [num(x) for x in w if x > 0 and x != r],
               "%d %s %d = %d. %s: %d %s %d = <b>%d</b>."
               % (a, MAL, k, a * k, "Noch %d-mal die %d dazu" % (b - k, a) if b > k else "%d-mal die %d weg" % (k - b, a),
                  a * k, "+" if b > k else "−", a * abs(b - k), r))


def div(lo_set):
    def mk():
        a = R.choice(lo_set)
        b = R.randint(2, 10)
        t = a * b
        w = [b + 1, b - 1, t - a, a, b * 2 if b * 2 != a else b + 2]
        return mcq("%d %s %d = ?" % (t, GETEILT, a), num(b), [num(x) for x in w if x > 0 and x != b],
                   "Denke an die Malaufgabe: %d %s ? = %d. Denn %d %s %d = %d. Ergebnis: <b>%d</b>." % (a, MAL, t, a, MAL, b, t, b))
    return mk


def platz():
    a = R.randint(3, 10)
    b = R.randint(2, 10)
    r = a * b
    kind = R.choice(["mal", "mal", "geteilt"])
    if kind == "mal":
        q = "%d %s ☐ = %d" % (a, MAL, r)
        ans = b
        w = [b + 1, b - 1, r - a, r // 2 if r % 2 == 0 and r // 2 != b else b + 2]
        e = "Welche Zahl mal %d ergibt %d? %d %s %d = %d, also ☐ = <b>%d</b>." % (a, r, a, MAL, b, r, b)
    else:
        q = "%d %s ☐ = %d" % (r, GETEILT, b)
        ans = a
        w = [a + 1, a - 1, r - b, b]
        e = "%d %s %d = %d, also ☐ = <b>%d</b>." % (r, GETEILT, a, b, a)
    return mcq("Welche Zahl fehlt? " + q, num(ans), [num(x) for x in w if x > 0 and x != ans], e)


def familie():
    a, b = R.sample(range(3, 10), 2)
    r = a * b
    ok = R.choice(["%d %s %d = %d" % (b, MAL, a, r), "%d %s %d = %d" % (r, GETEILT, a, b), "%d %s %d = %d" % (r, GETEILT, b, a)])
    bad = ["%d %s %d = %d" % (a, GETEILT, b, r), "%d %s %d = %d" % (r, GETEILT, a, a), "%d + %d = %d" % (a, b, r),
           "%d %s %d = %d" % (b, MAL, a, r + a), "%d %s %d = %d" % (r, MAL, a, b)]
    R.shuffle(bad)
    return mcq("Welche Aufgabe gehört zur Aufgabenfamilie von %d %s %d = %d?" % (a, MAL, b, r), ok, bad,
               "Zur Familie gehören die Tauschaufgabe %d %s %d = %d und die Geteiltaufgaben %d %s %d = %d und %d %s %d = %d. Richtig: <b>%s</b>."
               % (b, MAL, a, r, r, GETEILT, a, b, r, GETEILT, b, a, ok))


GROUPS = [
    ("In einen Eierkarton passen 6 Eier. Wie viele Eier sind in %d Kartons?", 6, "Eier"),
    ("Eine Woche hat 7 Tage. Wie viele Tage sind %d Wochen?", 7, "Tage"),
    ("Eine Spinne hat 8 Beine. Wie viele Beine haben %d Spinnen?", 8, "Beine"),
    ("Ein vierblättriges Kleeblatt hat 4 Blätter. Wie viele Blätter haben %d vierblättrige Kleeblätter?", 4, "Blätter"),
    ("Ein Dreirad hat 3 Räder. Wie viele Räder haben %d Dreiräder?", 3, "Räder"),
    ("In eine Packung passen 9 Würstchen. Wie viele Würstchen sind in %d Packungen?", 9, "Würstchen"),
    ("Ein Stift kostet 5 €. Wie viel kosten %d Stifte?", 5, "€"),
    ("An jedem Tisch sitzen 4 Kinder. Wie viele Kinder sitzen an %d Tischen?", 4, "Kinder"),
]
SHARE = [
    ("%d Kinder sollen gleich große Gruppen bilden. In jede Gruppe kommen %d Kinder. Wie viele Gruppen gibt es?", "Gruppen"),
    ("%d Bonbons werden an Kinder verteilt. Jedes Kind bekommt %d Bonbons. Wie viele Kinder bekommen Bonbons?", "Kinder"),
    ("%d Äpfel werden in Tüten gepackt. In jede Tüte kommen %d Äpfel. Wie viele Tüten braucht man?", "Tüten"),
]


def s5_sache():
    if R.random() < 0.6:
        t, k, u = R.choice(GROUPS)
        n = R.randint(3, 10)
        r = n * k
        w = [n + k, (n + 1) * k, (n - 1) * k, r + 1]
        return mcq(t % n, "%d %s" % (r, u), ["%d %s" % (x, u) for x in w if x > 0 and x != r],
                   "%d-mal %d: %d %s %d = <b>%d %s</b>." % (n, k, n, MAL, k, r, u))
    t, u = R.choice(SHARE)
    k, n = R.randint(3, 9), R.randint(3, 9)
    tot = k * n
    w = [n + 1, n - 1, tot - k, k if k != n else n + 2]
    return mcq(t % (tot, k), "%d %s" % (n, u), ["%d %s" % (x, u) for x in w if x > 0 and x != n],
               "%d %s %d = <b>%d</b>, denn %d %s %d = %d." % (tot, GETEILT, k, n, n, MAL, k, tot))


def main():
    seen = set()
    sets = [
        ("Kernaufgaben: 2, 5 und 10", mix(R, seen, [(mul([2, 5, 10]), 14), (mul([3, 4]), 6)])),
        ("Schwierige Reihen: 6, 7, 8 und 9", mix(R, seen, [(mul([6, 7, 8, 9]), 14), (nachbar, 6)])),
        ("Geteiltaufgaben", mix(R, seen, [(div([2, 3, 4, 5, 10]), 8), (div([6, 7, 8, 9]), 12)])),
        ("Platzhalter und Aufgabenfamilien", mix(R, seen, [(platz, 13), (familie, 7)])),
        ("Sachaufgaben zum Einmaleins", mix(R, seen, [(s5_sache, 20)])),
    ]
    body = lesson(
        ["Malnehmen heißt: gleich große Gruppen zusammenzählen. 4 %s 6 heißt 4-mal die 6: 6 + 6 + 6 + 6 = 24." % MAL,
         "Merke dir die <b>Kernaufgaben</b>: mal 1, mal 2, mal 5 und mal 10. Daraus findest du die anderen: 7 %s 9 = 7 %s 10 − 7 = 63." % (MAL, MAL),
         "Die <b>Tauschaufgabe</b> hat das gleiche Ergebnis: 3 %s 8 = 8 %s 3." % (MAL, MAL),
         "Geteilt ist die Umkehrung von mal: 56 %s 8 = 7, denn 7 %s 8 = 56." % (GETEILT, MAL)],
        [example("8 %s 6" % MAL, ["8 %s 5 = 40 (Kernaufgabe)" % MAL, "eine 8 mehr: 40 + 8 = 48"], "48"),
         example("63 %s 7" % GETEILT, ["Welche Zahl mal 7 ergibt 63?", "9 %s 7 = 63" % MAL], "9")],
        [["7 %s 8 = 15" % MAL, "Mal heißt nicht plus: 7 %s 8 = 56" % MAL],
         ["6 %s 7 = 48 (Nachbaraufgabe)" % MAL, "Von 6 %s 5 = 30 aus zweimal 6 dazu: 42" % MAL],
         ["24 %s 6 = 18" % GETEILT, "Geteilt heißt aufteilen: 24 %s 6 = 4, denn 4 %s 6 = 24" % (GETEILT, MAL)]])
    faq = [
        {"q": "Muss mein Kind das Einmaleins in Klasse 3 auswendig können?", "a": "Das kleine Einmaleins wird in Klasse 2 eingeführt und sollte in Klasse 3 sicher und schnell abrufbar sein, weil es für die Multiplikation und Division bis 1000 gebraucht wird."},
        {"q": "Welche Reihen sind am schwierigsten?", "a": "Meist die 6er-, 7er-, 8er- und 9er-Reihe. Hier helfen die Kernaufgaben (mal 5, mal 10) und Nachbaraufgaben."},
        {"q": "Warum schreibt man · statt ×?", "a": "In deutschen Grundschulen ist der Malpunkt (·) üblich. Für geteilt schreibt man einen Doppelpunkt (:)."},
        {"q": "Wie übt man am besten?", "a": "Täglich ein paar Minuten, gemischt statt nur in Reihen, und immer auch die passenden Geteiltaufgaben."},
    ]
    make_unit(R, "einmaleins", "Z",
              "Die Schülerinnen und Schüler beherrschen die Aufgaben des kleinen Einmaleins und die Umkehraufgaben automatisiert und nutzen Rechengesetze und Ableitungsstrategien (Zusammenfassung).",
              "Das kleine Einmaleins: Mal- und Geteiltaufgaben",
              "Einmaleins üben Klasse 3 – Arbeitsblätter mit Lösungen",
              "Einmaleins",
              "Das kleine Einmaleins für Klasse 3: alle Reihen, Geteiltaufgaben, Platzhalter, Aufgabenfamilien und Sachaufgaben. 100 Übungsaufgaben mit Lösungen und Arbeitsblatt zum Ausdrucken, kostenlos.",
              "Mal heißt gleich große Gruppen.",
              "Kernaufgaben (mal 2, 5, 10) helfen bei den schweren Reihen.",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
