# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Schriftlich addieren und subtrahieren bis 1 Million（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k4_schriftlich_addieren_und_subtrahieren.py
Addition mit mehreren Überträgen, drei Summanden, Subtraktion mit Entbündeln (auch über Nullen), Probe, Sachaufgaben.
Fehler: Übertrag vergessen, kleine von großer Ziffer abziehen, Stellen verrutscht, beim Entbündeln über Nullen die Null nicht verringert.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, schriftlich, Kids

R = random.Random(49103)
KIDS = Kids(R)


def cols(n, w=6):
    return [int(d) for d in str(n).rjust(w, "0")][::-1]


def no_carry(nums):
    out = [sum(cols(x)[k] for x in nums) % 10 for k in range(6)]
    return int("".join(str(d) for d in out[::-1]))


def n_carry(nums):
    c, n = 0, 0
    for k in range(6):
        s = sum(cols(x)[k] for x in nums) + c
        c = s // 10
        n += 1 if c else 0
    return n


def small_big(a, b):
    return int("".join(str(abs(cols(a)[k] - cols(b)[k])) for k in range(5, -1, -1)))


def no_reduce(a, b):
    out = []
    for k in range(6):
        x, y = cols(a)[k], cols(b)[k]
        out.append((x + 10 - y) % 10 if x < y else x - y)
    return int("".join(str(d) for d in out[::-1]))


def add(n_sum, lo, hi):
    def mk():
        nums = [R.randint(lo, hi) for _ in range(n_sum)]
        if R.random() < 0.25 and n_sum == 2:
            nums[1] = R.randint(lo // 10, hi // 10)
        r = sum(nums)
        if r >= 1000000 or n_carry(nums) < 2:
            return None
        w = [no_carry(nums), r + 1000, r - 10, r + 100, r + 10000]
        if n_sum == 2 and nums[1] < lo:
            w.insert(0, nums[0] + nums[1] * 10)
        return mcq(schriftlich([str(x) for x in nums]) + "Rechne schriftlich: %s" % " + ".join(num(x) for x in nums), num(r),
                   [num(x) for x in w if 0 < x < 1000000 and x != r],
                   "Stellengerecht untereinander, von rechts nach links, Überträge mitrechnen. Ergebnis: <b>%s</b>." % num(r))
    return mk


def sub(zero=False):
    def mk():
        if zero:
            a = R.choice([R.randint(1, 9) * 100000 + R.randint(1, 9) * 100, R.randint(1, 9) * 100000, R.randint(10, 99) * 10000 + R.randint(1, 9)])
        else:
            a = R.randint(20000, 999999)
        b = R.randint(1000, a - 500)
        r = a - b
        sb, nr = small_big(a, b), no_reduce(a, b)
        if sb == r:
            return None
        w = [sb, nr, r + 1000, r - 10, r + 100]
        return mcq(schriftlich([str(a), str(b)], op="−") + "Rechne schriftlich: %s − %s" % (num(a), num(b)), num(r),
                   [num(x) for x in w if 0 < x < 1000000 and x != r],
                   "Von rechts nach links, bei Bedarf entbündeln%s. Ergebnis: <b>%s</b>. Probe: %s + %s = %s."
                   % (" (auch über Nullen hinweg)" if zero else "", num(r), num(r), num(b), num(a)))
    return mk


def luecke():
    a, b = R.randint(10000, 600000), R.randint(10000, 390000)
    r = a + b
    s = str(r)
    k = R.randint(1, len(s) - 1)
    d = int(s[k])
    shown = num(int(s[:k] + "0" + s[k + 1:])).replace(" ", " ")
    # die Lücke an der richtigen Stelle anzeigen
    digits = list(s)
    digits[k] = "☐"
    grp = "".join(digits)
    out = []
    while grp:
        out.insert(0, grp[-3:])
        grp = grp[:-3]
    shown = " ".join(out)
    w = [(d + 1) % 10, (d - 1) % 10, (d + 2) % 10, int(str(no_carry([a, b])).rjust(len(s), "0")[k]) if len(str(no_carry([a, b]))) == len(s) else (d + 3) % 10]
    return mcq("Welche Ziffer fehlt im Ergebnis? %s + %s = %s" % (num(a), num(b), shown), str(d), [str(x) for x in w if x != d],
               "%s + %s = %s. Die fehlende Ziffer ist <b>%d</b>." % (num(a), num(b), num(r), d))


def probe():
    a = R.randint(50000, 900000)
    b = R.randint(10000, a - 5000)
    r = a - b
    claim = R.choice([r, r + 1000, r - 100, small_big(a, b) if small_big(a, b) != r else r + 10])
    ok = claim == r
    q = "Ben rechnet %s − %s = %s. Mache die Probe. Stimmt das?" % (num(a), num(b), num(claim))
    s = claim + b
    ans = "%s + %s = %s, also %s" % (num(claim), num(b), num(s), "richtig" if ok else "falsch")
    w = ["%s + %s = %s, also %s" % (num(claim), num(b), num(s), "falsch" if ok else "richtig"),
         "%s + %s = %s, also richtig" % (num(a), num(b), num(a + b)), "%s − %s = %s, also %s" % (num(a), num(claim), num(a - claim), "falsch" if ok else "richtig")]
    return mcq(q, ans, w, "Ergebnis + abgezogene Zahl muss die erste Zahl ergeben: <b>%s</b>." % ans)


def sache():
    kind = R.choice(["besucher", "einwohner", "auto", "spenden", "km"])
    if kind == "besucher":
        a, b, c = R.randint(12000, 48000), R.randint(12000, 48000), R.randint(12000, 48000)
        r = a + b + c
        q = "Ein Freizeitpark hatte im Juni %s, im Juli %s und im August %s Besucher. Wie viele Besucher waren es zusammen?" % (num(a), num(b), num(c))
        w = [no_carry([a, b, c]), r + 1000, a + b, r - 10]
    elif kind == "einwohner":
        a = R.randint(150000, 900000)
        b = R.randint(a // 8, a // 5)
        r = a - b
        q = "Eine Stadt hat %s Einwohner. %s davon sind Kinder und Jugendliche. Wie viele Erwachsene leben dort?" % (num(a), num(b))
        w = [small_big(a, b), no_reduce(a, b), a + b, r + 1000]
        return mcq(q, num(r), [num(x) for x in w if 0 < x < 1000000 and x != r], "%s − %s = <b>%s</b>." % (num(a), num(b), num(r)))
    elif kind == "auto":
        a = R.randint(18000, 45000)
        b = R.randint(8000, 30000)
        r = a + b
        q = "Ein Auto hat %s km auf dem Tacho. In einem Jahr fährt es noch %s km. Welcher Kilometerstand steht dann auf dem Tacho?" % (num(a), num(b))
        w = [no_carry([a, b]), r + 1000, a - b, r - 100]
        r_u = "km"
        return mcq(q, "%s km" % num(r), ["%s km" % num(x) for x in w if x > 0 and x != r], "%s + %s = <b>%s km</b>." % (num(a), num(b), num(r)))
    elif kind == "spenden":
        goal = R.choice([100000, 250000, 500000])
        have = R.randint(goal // 4, goal - 5000)
        r = goal - have
        q = "Für einen neuen Spielplatz werden %s € gebraucht. %s € sind schon da. Wie viel Geld fehlt noch?" % (num(goal), num(have))
        w = [small_big(goal, have), no_reduce(goal, have), r + 1000, have]
        return mcq(q, "%s €" % num(r), ["%s €" % num(x) for x in w if x > 0 and x != r], "%s − %s = <b>%s €</b>." % (num(goal), num(have), num(r)))
    else:
        a, b = R.randint(1200, 9800), R.randint(1200, 9800)
        r = a + b
        q = "Ein Flugzeug fliegt %s km nach New York und %s km weiter nach Mexiko-Stadt. Wie weit fliegt es insgesamt?" % (num(a), num(b))
        w = [no_carry([a, b]), r + 1000, abs(a - b), r - 100]
        return mcq(q, "%s km" % num(r), ["%s km" % num(x) for x in w if x > 0 and x != r], "%s + %s = <b>%s km</b>." % (num(a), num(b), num(r)))
    return mcq(q, num(r), [num(x) for x in w if x > 0 and x != r], "%s + %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(r)))


def main():
    seen = set()
    sets = [
        ("Schriftlich addieren", mix(R, seen, [(add(2, 10000, 500000), 20)])),
        ("Drei Zahlen addieren", mix(R, seen, [(add(3, 10000, 300000), 14), (luecke, 6)])),
        ("Schriftlich subtrahieren", mix(R, seen, [(sub(), 20)])),
        ("Subtrahieren über Nullen und Probe", mix(R, seen, [(sub(True), 14), (probe, 6)])),
        ("Sachaufgaben mit großen Zahlen", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Schreibe die Zahlen <b>stellengerecht</b> untereinander: Einer unter Einer, Tausender unter Tausender.",
         "Rechne von rechts nach links. Bei der Addition schreibst du Überträge klein in die nächste Spalte.",
         "Bei der Subtraktion entbündelst du, wenn oben zu wenig steht. Steht links eine 0, entbündelst du von der nächsten Stelle mit einer Ziffer.",
         "Mache vorher einen Überschlag und danach die Probe."],
        [example("45 678 + 28 945", ["8 + 5 = 13 → 3, Übertrag 1", "7 + 4 + 1 = 12 → 2, Übertrag 1", "6 + 9 + 1 = 16 → 6, Übertrag 1", "5 + 8 + 1 = 14 → 4, Übertrag 1", "4 + 2 + 1 = 7"], "74 623"),
         example("500 000 − 123 456", ["über die Nullen entbündeln: 4 9 9 9 9 10", "10 − 6 = 4, 9 − 5 = 4, 9 − 4 = 5, 9 − 3 = 6, 9 − 2 = 7, 4 − 1 = 3"], "376 544")],
        [["Übertrag vergessen", "Den kleinen Übertrag in der nächsten Spalte mitrechnen"],
         ["45 678 + 2 894 untereinander linksbündig", "Rechtsbündig: Einer unter Einer"],
         ["500 000 − 123 456: bei den Nullen nichts entbündeln", "Erst einen Hunderttausender in 10 Zehntausender tauschen, dann weiter"]])
    faq = [
        {"q": "Wie viele Stellen rechnen Kinder in Klasse 4 schriftlich?", "a": "Bis zu sechs Stellen, also im Zahlenraum bis zur Million, auch mit mehreren Summanden."},
        {"q": "Warum ist 500 000 − 123 456 schwierig?", "a": "Weil über mehrere Nullen entbündelt werden muss. Am besten schreibt man die neuen Ziffern deutlich über die Nullen."},
        {"q": "Wie macht man die Probe?", "a": "Bei Minusaufgaben addiert man das Ergebnis und die abgezogene Zahl. Bei Plusaufgaben zieht man einen Summanden vom Ergebnis ab."},
        {"q": "Welches Verfahren nutzt die Schule?", "a": "Je nach Bundesland Abziehen mit Entbündeln oder Ergänzen. Die Ergebnisse sind gleich."},
    ]
    make_unit(R, "schriftlich-addieren-und-subtrahieren", "Z",
              "Die Schülerinnen und Schüler führen die schriftliche Addition und Subtraktion im Zahlenraum bis zur Million sicher aus und kontrollieren mit Überschlag und Umkehraufgabe (Zusammenfassung).",
              "Schriftlich addieren und subtrahieren bis 1 Million",
              "Schriftliche Addition und Subtraktion Klasse 4 – Arbeitsblätter mit Lösungen",
              "Schriftlich plus und minus",
              "Klasse 4: schriftliche Addition und Subtraktion mit großen Zahlen, drei Summanden, Entbündeln über Nullen, Probe und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Stellengerecht untereinander, von rechts nach links.",
              "Überschlag vorher, Probe danach.",
              body, faq, sets, 3, grade="klasse-4")


if __name__ == "__main__":
    main()
