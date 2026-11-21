# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Schriftliche Addition（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_schriftliche_addition.py
Ohne Übertrag, mit einem und zwei Überträgen, drei Zahlen, fehlende Ziffern, Sachaufgaben mit Überschlag.
Fehler: Übertrag vergessen (345 + 238 → 573), Stellen verrutscht (345 + 42 → 765), Übertrag doppelt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, schriftlich, Kids

R = random.Random(49005)
KIDS = Kids(R)


def cols(n):
    return [int(d) for d in str(n).rjust(3, "0")][::-1]


def carries(nums):
    """Überträge (Stelle von rechts: Ziffer) und Anzahl"""
    out, c = {}, 0
    for k in range(3):
        s = sum(cols(x)[k] for x in nums) + c
        c = s // 10
        if c and k < 2:
            out[k + 1] = c
    return out


def no_carry(nums):
    return int("".join(str(sum(cols(x)[k] for x in nums) % 10) for k in (2, 1, 0)))


def task(nums, need):
    """need: Anzahl der Überträge"""
    if sum(nums) > 1000 or len(carries(nums)) != need:
        return None
    r = sum(nums)
    w = [no_carry(nums) if need else None, r + 10, r - 10, r + 100, r - 100 if r > 200 else r + 1, r + 1]
    if any(x < 100 for x in nums):
        small = [x for x in nums if x < 100][0]
        w.insert(0, r - small + small * 10)
    pic = schriftlich([str(x) for x in nums])
    cs = carries(nums)
    e = "Von rechts nach links rechnen: Einer, Zehner, Hunderter."
    if cs:
        e += " Überträge: %s." % ", ".join("1 %s weiter" % ("Zehner" if k == 1 else "Hunderter") for k in sorted(cs))
    e += " Ergebnis: <b>%s</b>." % num(r)
    return mcq(pic + "Rechne schriftlich: %s" % " + ".join(num(x) for x in nums), num(r), [num(x) for x in w if x and 0 < x <= 1000 and x != r], e)


def s1():
    a, b = R.randint(101, 788), R.randint(101, 499)
    return task([a, b], 0)


def s2():
    a, b = R.randint(105, 689), R.randint(105, 489)
    if R.random() < 0.25:
        b = R.randint(12, 89)
    return task([a, b], 1)


def s3():
    a, b = R.randint(156, 589), R.randint(156, 489)
    return task([a, b], 2)


def s4_drei():
    a, b, c = R.randint(101, 399), R.randint(101, 399), R.randint(12, 299)
    if a + b + c > 1000:
        return None
    nums = [a, b, c]
    n = len(carries(nums))
    if n == 0:
        return None
    r = sum(nums)
    pic = schriftlich([str(x) for x in nums])
    col0 = sum(cols(x)[0] for x in nums)
    w = [no_carry(nums), r + 10, r - 10, r + 100, r + 20 if col0 >= 20 else r - 20]
    return mcq(pic + "Rechne schriftlich: %s" % " + ".join(num(x) for x in nums), num(r), [num(x) for x in w if 0 < x <= 1000 and x != r],
               "Einer: %s = %d. %s Ergebnis: <b>%s</b>." % (" + ".join(str(cols(x)[0]) for x in nums), col0,
                                                           "Schreibe %d, übertrage %d." % (col0 % 10, col0 // 10) if col0 >= 10 else "Kein Übertrag bei den Einern.", num(r)))


def s4_luecke():
    a, b = R.randint(120, 589), R.randint(120, 389)
    r = a + b
    if r > 999:
        return None
    pos = R.choice([0, 1])
    k = R.choice([0, 1])  # Stelle: 0 = Zehner, 1 = Einer
    s = str(a) if pos == 0 else str(b)
    i = 1 if k == 0 else 2
    d = int(s[i])
    shown = s[:i] + "☐" + s[i + 1:]
    q = ("Welche Ziffer fehlt? %s + %s = %s" % (shown, num(b), num(r)) if pos == 0 else
         "Welche Ziffer fehlt? %s + %s = %s" % (num(a), shown, num(r)))
    w = [(d + 1) % 10, (d - 1) % 10, (d + 2) % 10, 9 - d]
    return mcq(q, str(d), [str(x) for x in w if x != d],
               "Setze %d ein und prüfe: %s + %s = %s. Die fehlende Ziffer ist <b>%d</b>." % (d, num(a), num(b), num(r), d))


THINGS = [
    ("Bücherei", "Im Januar leiht die Bücherei %s Bücher aus, im Februar %s Bücher. Wie viele Bücher sind es zusammen?", "Bücher"),
    ("Saft", "Ein Getränkemarkt verkauft am Freitag %s Flaschen Saft und am Samstag %s Flaschen. Wie viele Flaschen sind es zusammen?", "Flaschen"),
    ("Fahrt", "Familie Yilmaz fährt am ersten Tag %s km und am zweiten Tag %s km. Wie weit fährt sie insgesamt?", "km"),
    ("Schule", "An der Grundschule sind %s Mädchen und %s Jungen. Wie viele Kinder sind es zusammen?", "Kinder"),
    ("Konzert", "Beim Schulkonzert werden am Vormittag %s Karten und am Nachmittag %s Karten verkauft. Wie viele Karten sind es?", "Karten"),
]


def s5_sache():
    kind = R.choice(["zwei", "zwei", "drei", "preis"])
    if kind == "zwei":
        t = R.choice(THINGS)
        a, b = R.randint(156, 589), R.randint(156, 389)
        if a + b > 1000 or not carries([a, b]):
            return None
        r = a + b
        w = [no_carry([a, b]), r + 10, r - 100, abs(a - b)]
        return mcq(t[1] % (num(a), num(b)), "%s %s" % (num(r), t[2]), ["%s %s" % (num(x), t[2]) for x in w if x > 0 and x != r],
                   "%s + %s = <b>%s %s</b>." % (num(a), num(b), num(r), t[2]))
    if kind == "drei":
        a, b, c = R.randint(110, 320), R.randint(110, 320), R.randint(110, 320)
        if a + b + c > 1000 or not carries([a, b, c]):
            return None
        r = a + b + c
        q = "Beim Sponsorenlauf sammelt die Klasse 3a %s €, die 3b %s € und die 3c %s €. Wie viel Geld ist es zusammen?" % (num(a), num(b), num(c))
        w = [no_carry([a, b, c]), a + b, r + 10, r - 10]
        return mcq(q, "%s €" % num(r), ["%s €" % num(x) for x in w if x > 0 and x != r],
                   "Alle drei Beträge schriftlich untereinander: %s + %s + %s = <b>%s €</b>." % (num(a), num(b), num(c), num(r)))
    p = KIDS.next()
    a, b = R.randint(160, 590), R.randint(60, 380)
    if a + b > 1000 or not carries([a, b]):
        return None
    r = a + b
    q = "%s kauft ein Fahrrad für %s € und ein Schloss mit Helm für %s €. Wie viel muss %s bezahlen?" % (p[0], num(a), num(b), p[1])
    w = [no_carry([a, b]), r + 100, r - 10, a - b]
    return mcq(q, "%s €" % num(r), ["%s €" % num(x) for x in w if x > 0 and x != r],
               "%s + %s = <b>%s €</b>. Überschlag: etwa %s + %s = %s." % (num(a), num(b), num(r), num((a + 50) // 100 * 100), num((b + 50) // 100 * 100),
                                                                       num((a + 50) // 100 * 100 + (b + 50) // 100 * 100)))


def main():
    seen = set()
    sets = [
        ("Ohne Übertrag", mix(R, seen, [(s1, 20)])),
        ("Mit einem Übertrag", mix(R, seen, [(s2, 20)])),
        ("Mit zwei Überträgen", mix(R, seen, [(s3, 20)])),
        ("Drei Zahlen und fehlende Ziffern", mix(R, seen, [(s4_drei, 12), (s4_luecke, 8)])),
        ("Sachaufgaben", mix(R, seen, [(s5_sache, 20)])),
    ]
    body = lesson(
        ["Schreibe die Zahlen genau <b>untereinander</b>: Einer unter Einer, Zehner unter Zehner, Hunderter unter Hunderter.",
         "Rechne von <b>rechts nach links</b>: zuerst die Einer, dann die Zehner, dann die Hunderter.",
         "Ist eine Summe 10 oder mehr, schreibst du die Einer hin und den <b>Übertrag</b> klein in die nächste Spalte.",
         "Mache vorher einen <b>Überschlag</b>. So merkst du, wenn etwas nicht stimmen kann."],
        [example("345 + 238",
                 ["Einer: 5 + 8 = 13 → schreibe 3, übertrage 1", "Zehner: 4 + 3 + 1 = 8", "Hunderter: 3 + 2 = 5"], "583"),
         example("467 + 285", ["Einer: 7 + 5 = 12 → 2, Übertrag 1", "Zehner: 6 + 8 + 1 = 15 → 5, Übertrag 1", "Hunderter: 4 + 2 + 1 = 7"], "752")],
        [["Übertrag vergessen: 345 + 238 = 573", "Den kleinen Übertrag in der nächsten Spalte mitrechnen: 583"],
         ["Stellen verrutscht: 345 + 42 = 765", "Einer unter Einer schreiben: 345 + 42 = 387"],
         ["Links anfangen", "Immer bei den Einern (rechts) beginnen"]],
        extra=schriftlich(["345", "238"], carries={1: 1}, result="583"))
    faq = [
        {"q": "Wann lernen Kinder die schriftliche Addition?", "a": "In den meisten Bundesländern in Klasse 3, nach dem halbschriftlichen Rechnen im Zahlenraum bis 1000."},
        {"q": "Wohin schreibt man den Übertrag?", "a": "Klein in die nächste Spalte links, meist direkt über die Linie. Er wird in dieser Spalte mitgerechnet."},
        {"q": "Wie viele Zahlen darf man untereinander schreiben?", "a": "Beliebig viele. In Klasse 3 übt man meist zwei oder drei Zahlen."},
        {"q": "Wie kann mein Kind das Ergebnis prüfen?", "a": "Mit einem Überschlag (gerundete Zahlen) oder mit der Umkehraufgabe (Ergebnis minus eine Zahl)."},
    ]
    make_unit(R, "schriftliche-addition", "Z",
              "Die Schülerinnen und Schüler führen die schriftliche Addition im Zahlenraum bis 1000 sicher aus, verstehen den Übertrag als Bündeln und kontrollieren mit einem Überschlag (Zusammenfassung).",
              "Schriftliche Addition mit Übertrag",
              "Schriftliche Addition Klasse 3 – Arbeitsblätter mit Lösungen",
              "Schriftliche Addition",
              "Schriftliche Addition für Klasse 3: ohne und mit Übertrag, drei Zahlen, fehlende Ziffern und Sachaufgaben. 100 Übungsaufgaben mit Lösungen und Arbeitsblatt zum Ausdrucken, kostenlos.",
              "Einer unter Einer, von rechts nach links.",
              "Ab 10 schreibst du die Einer hin und überträgst 1 in die nächste Spalte.",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
