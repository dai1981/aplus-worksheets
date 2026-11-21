# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Plus und Minus bis 1000 – Kopfrechnen und halbschriftlich（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_plus_und_minus_bis_1000.py
Hunderter- und Zehnerzahlen, Zehner- und Hunderterübergang, halbschriftliche Addition und Subtraktion, Ergänzen, Sachaufgaben.
Fehler: Übertrag vergessen (345 + 238 → 573), „kleine von großer Ziffer“ (632 − 257 → 425), um einen Zehner verrechnet.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids

R = random.Random(49004)
KIDS = Kids(R)


def digits(n):
    return n // 100, n // 10 % 10, n % 10


def no_carry_add(a, b):
    """stellenweise addieren ohne Übertrag"""
    return int("".join(str((int(x) + int(y)) % 10) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0")))) + (1000 if a + b >= 1000 else 0)


def small_from_big(a, b):
    """stellenweise die kleinere von der größeren Ziffer abziehen"""
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0"))))


# ---------------------------------------------------------------- Runde 1
def s1_ganze():
    kind = R.choice(["H+H", "H-H", "HZ+Z", "HZ-Z", "HZ+H", "HZ-H"])
    if kind == "H+H":
        a, b = R.randint(1, 8) * 100, None
        b = R.randint(1, 10 - a // 100) * 100
        op, r = "+", a + b
    elif kind == "H-H":
        a = R.randint(3, 10) * 100
        b = R.randint(1, a // 100 - 1) * 100
        op, r = "−", a - b
    elif kind == "HZ+Z":
        a = R.randint(1, 9) * 100 + R.randint(1, 8) * 10
        b = R.randint(1, 9 - a // 10 % 10) * 10
        op, r = "+", a + b
    elif kind == "HZ-Z":
        a = R.randint(1, 9) * 100 + R.randint(2, 9) * 10
        b = R.randint(1, a // 10 % 10) * 10
        op, r = "−", a - b
    elif kind == "HZ+H":
        a = R.randint(1, 8) * 100 + R.randint(1, 9) * 10
        b = R.randint(1, 9 - a // 100) * 100
        op, r = "+", a + b
    else:
        a = R.randint(3, 9) * 100 + R.randint(1, 9) * 10
        b = R.randint(1, a // 100 - 1) * 100
        op, r = "−", a - b
    if r <= 0 or r > 1000 or b <= 0:
        return None
    big = b >= 100
    w = [r + 10, r - 10, r + 100, r - 100, (a + b // 10) if op == "+" and big else (a - b // 10 if big else (a + b * 10 if op == "+" else a - b * 10))]
    return mcq("%s %s %s = ?" % (num(a), op, num(b)), num(r), [num(x) for x in w if 0 < x <= 1000 and x != r],
               "Rechne mit %s: %s %s %s = <b>%s</b>." % ("den Hundertern" if big else "den Zehnern", num(a), op, num(b), num(r)))


def s1_einer():
    a = R.randint(101, 989)
    op = R.choice(["+", "−"])
    if op == "+":
        b = R.randint(1, 9 - a % 10) if a % 10 < 9 else None
    else:
        b = R.randint(1, a % 10) if a % 10 else None
    if not b:
        return None
    r = a + b if op == "+" else a - b
    w = [r + 10, r - 10 if r > 10 else r + 20, r + 1, r - 1, a + 10 * b if op == "+" else a - 10 * b]
    return mcq("%s %s %d = ?" % (num(a), op, b), num(r), [num(x) for x in w if 0 < x < 1000 and x != r],
               "Nur die Einer ändern sich: %s %s %d = <b>%s</b>." % (num(a), op, b, num(r)))


# ---------------------------------------------------------------- Runde 2: Übergang
def s2_uebergang():
    kind = R.choice(["Z+", "Z-", "E+", "E-"])
    if kind == "Z+":
        a = R.randint(1, 8) * 100 + R.randint(3, 9) * 10
        b = R.randint(10 - a // 10 % 10 + 1, 9) * 10 if a // 10 % 10 >= 2 else None
        op = "+"
    elif kind == "Z-":
        a = R.randint(2, 9) * 100 + R.randint(0, 6) * 10
        b = R.randint(a // 10 % 10 + 1, 9) * 10
        op = "−"
    elif kind == "E+":
        a = R.randint(10, 98) * 10 + R.randint(3, 9)
        b = R.randint(10 - a % 10, 9)
        op = "+"
    else:
        a = R.randint(10, 99) * 10 + R.randint(0, 6)
        b = R.randint(a % 10 + 1, 9)
        op = "−"
    if not b:
        return None
    r = a + b if op == "+" else a - b
    if r > 1000 or r <= 0:
        return None
    step = 100 if kind[0] == "Z" else 10
    w = [r - step if op == "+" else r + step, r + 10 if kind[0] == "Z" else r + 1, r - 10 if kind[0] == "Z" else r - 1,
         r + step if op == "+" else r - step]
    if kind[0] == "Z":
        to = (a // 100 + (1 if op == "+" else 0)) * 100
        first = abs(to - a)
        e = ("Erst bis zum Hunderter: %s %s %s = %s, dann noch %s: <b>%s</b>." % (num(a), op, num(first), num(to), num(b - first), num(r))
             if first else "%s %s %s = <b>%s</b>." % (num(a), op, num(b), num(r)))
    else:
        to = (a // 10 + (1 if op == "+" else 0)) * 10
        first = abs(to - a)
        e = ("Erst bis zum Zehner: %s %s %d = %s, dann noch %d: <b>%s</b>." % (num(a), op, first, num(to), b - first, num(r))
             if first else "%s %s %d = <b>%s</b>." % (num(a), op, b, num(r)))
    return mcq("%s %s %s = ?" % (num(a), op, num(b)), num(r), [num(x) for x in w if 0 < x <= 1000 and x != r], e)


# ---------------------------------------------------------------- Runde 3/4: halbschriftlich
def s3_add():
    a = R.randint(112, 689)
    b = R.randint(112, 980 - a)
    if b < 100:
        return None
    r = a + b
    nc = no_carry_add(a, b)
    if nc == r:
        return None
    ha, za, ea = digits(a)
    hb, zb, eb = digits(b)
    w = [nc, r + 10, r - 10, r + 100]
    e = ("Schrittweise: %s + %s = %s, + %s = %s, + %d = <b>%s</b>."
         % (num(a), num(100 * hb), num(a + 100 * hb), num(10 * zb), num(a + 100 * hb + 10 * zb), eb, num(r)))
    return mcq("Rechne: %s + %s" % (num(a), num(b)), num(r), [num(x) for x in w if 0 < x <= 1000 and x != r], e)


def s4_sub():
    a = R.randint(320, 980)
    b = R.randint(110, a - 100)
    r = a - b
    sb = small_from_big(a, b)
    if sb == r and (a % 10 >= b % 10 and a // 10 % 10 >= b // 10 % 10):
        return None
    hb, zb, eb = digits(b)
    w = [sb if sb != r else None, r + 10, r - 10, r + 100]
    e = ("Schrittweise: %s − %s = %s, − %s = %s, − %d = <b>%s</b>."
         % (num(a), num(100 * hb), num(a - 100 * hb), num(10 * zb), num(a - 100 * hb - 10 * zb), eb, num(r)))
    return mcq("Rechne: %s − %s" % (num(a), num(b)), num(r), [num(x) for x in w if x and 0 < x <= 1000 and x != r], e)


def s4_umkehr():
    a = R.randint(150, 900)
    b = R.randint(110, a - 30)
    r = a - b
    q = "Ida rechnet %s − %s = %s. Mit welcher Aufgabe kann sie das prüfen?" % (num(a), num(b), num(r))
    ans = "%s + %s = %s" % (num(r), num(b), num(a))
    w = ["%s + %s = %s" % (num(a), num(b), num(a + b)),
         "%s − %s = %s" % (num(max(r, b)), num(min(r, b)), num(abs(r - b))) if r != b else "%s + %s = %s" % (num(b), num(b), num(2 * b)),
         "%s + %s = %s" % (num(r), num(a), num(r + a))]
    return mcq(q, ans, w, "Die Umkehraufgabe zu Minus ist Plus: Ergebnis + abgezogene Zahl = Anfangszahl. <b>%s</b>." % ans)


# ---------------------------------------------------------------- Runde 5: Ergänzen und Sachaufgaben
def s5_ergaenzen():
    kind = R.choice(["1000", "H", "frei"])
    if kind == "1000":
        a = R.randint(10, 98) * 10 + R.choice([0, 0, R.randint(1, 9)])
        t = 1000
    elif kind == "H":
        a = R.randint(101, 899)
        t = (a // 100 + 1) * 100
        if a % 100 == 0:
            return None
    else:
        a = R.randint(150, 700)
        t = a + R.randint(120, 290)
    d = t - a
    w = [d + 10, d - 10 if d > 10 else d + 20, d + 100 if d + 100 < t else d + 1,
         int(str(1000 - a)[:-1] + "0") if kind == "1000" and a % 10 else d + 2]
    return mcq("Ergänze: %s + ☐ = %s" % (num(a), num(t)), num(d), [num(x) for x in w if x > 0 and x != d],
               "Rechne von %s bis %s: %s − %s = <b>%s</b>." % (num(a), num(t), num(t), num(a), num(d)))


def s5_sache():
    kind = R.choice(["zug", "spenden", "seiten", "bus", "laufen"])
    p = KIDS.next()
    if kind == "zug":
        a, b, c = R.randint(250, 520), R.randint(40, 140), R.randint(30, 160)
        r = a - b + c
        q = "In einem Zug sitzen %s Fahrgäste. In Kassel steigen %s aus und %s ein. Wie viele Fahrgäste sind jetzt im Zug?" % (num(a), num(b), num(c))
        w = [a + b + c, a - b - c, a + b - c, r + 10]
        e = "%s − %s = %s, dann + %s = <b>%s</b>." % (num(a), num(b), num(a - b), num(c), num(r))
        return mcq(q, num(r), [num(x) for x in w if 0 < x <= 1000 and x != r], e)
    if kind == "spenden":
        a, b = R.randint(180, 520), R.randint(150, 450)
        if a + b > 1000:
            return None
        r = a + b
        q = "Die Klasse 3a sammelt %s Kastanien, die Klasse 3b %s Kastanien. Wie viele Kastanien sind es zusammen?" % (num(a), num(b))
        w = [no_carry_add(a, b), r + 10, r - 100, abs(a - b)]
        return mcq(q, "%s Kastanien" % num(r), ["%s Kastanien" % num(x) for x in w if x > 0 and x != r],
                   "%s + %s = <b>%s Kastanien</b>." % (num(a), num(b), num(r)))
    if kind == "seiten":
        a = R.randint(200, 480)
        b = R.randint(60, a - 60)
        r = a - b
        q = "Ein Buch hat %s Seiten. %s hat schon %s Seiten gelesen. Wie viele Seiten fehlen noch?" % (num(a), p[0], num(b))
        w = [a + b, small_from_big(a, b) if small_from_big(a, b) != r else r + 1, r + 10, r - 10]
        return mcq(q, "%s Seiten" % num(r), ["%s Seiten" % num(x) for x in w if 0 < x <= 1000 and x != r],
                   "%s − %s = <b>%s Seiten</b>." % (num(a), num(b), num(r)))
    if kind == "bus":
        a = R.randint(320, 760)
        r = 1000 - a
        q = "%s spart für ein Tablet. Es kostet 1000 €. %s hat schon %s €. Wie viel Geld fehlt noch?" % (p[0], p[1].capitalize(), num(a))
        w = [r + 10, r - 10, r + 100, 900 - a if a < 900 else r + 2]
        return mcq(q, "%s €" % num(r), ["%s €" % num(x) for x in w if x > 0 and x != r],
                   "Ergänze von %s bis 1000: <b>%s €</b>." % (num(a), num(r)))
    a, b = R.randint(250, 480), R.randint(250, 480)
    if a + b > 1000 or a == b:
        return None
    q = "Beim Sponsorenlauf läuft %s am Vormittag %s m und am Nachmittag %s m. Wie viele Meter sind es zusammen?" % (p[0], num(a), num(b))
    r = a + b
    w = [no_carry_add(a, b), r + 100, r - 10, abs(a - b)]
    return mcq(q, "%s m" % num(r), ["%s m" % num(x) for x in w if x > 0 and x != r], "%s + %s = <b>%s m</b>." % (num(a), num(b), num(r)))


def main():
    seen = set()
    sets = [
        ("Mit Hundertern, Zehnern und Einern", mix(R, seen, [(s1_ganze, 14), (s1_einer, 6)])),
        ("Über den Zehner und den Hunderter", mix(R, seen, [(s2_uebergang, 20)])),
        ("Halbschriftlich addieren", mix(R, seen, [(s3_add, 20)])),
        ("Halbschriftlich subtrahieren", mix(R, seen, [(s4_sub, 15), (s4_umkehr, 5)])),
        ("Ergänzen und Sachaufgaben", mix(R, seen, [(s5_ergaenzen, 6), (s5_sache, 14)])),
    ]
    body = lesson(
        ["Mit Hunderterzahlen rechnest du wie mit Einern: 3 + 4 = 7, also 300 + 400 = 700.",
         "Beim <b>Zehnerübergang</b> rechnest du erst bis zum nächsten Zehner, dann weiter: 386 + 7 = 386 + 4 + 3 = 393.",
         "<b>Halbschriftlich</b> rechnest du in Schritten: erst die Hunderter, dann die Zehner, dann die Einer.",
         "Prüfe Minusaufgaben mit der <b>Umkehraufgabe</b>: 632 − 257 = 375, denn 375 + 257 = 632."],
        [example("345 + 238", ["345 + 200 = 545", "545 + 30 = 575", "575 + 8 = 583"], "583"),
         example("632 − 257", ["632 − 200 = 432", "432 − 50 = 382", "382 − 7 = 375"], "375")],
        [["345 + 238 = 573 (Übertrag vergessen)", "5 + 8 = 13: 1 Zehner weiter → 583"],
         ["632 − 257 = 425 (kleine von großer Ziffer)", "In Schritten abziehen: 632 − 200 − 50 − 7 = 375"],
         ["Im Zug: aussteigen addieren", "Aussteigen heißt minus, einsteigen heißt plus"]])
    faq = [
        {"q": "Was heißt halbschriftlich rechnen?", "a": "Man schreibt Zwischenschritte auf und rechnet zum Beispiel erst die Hunderter, dann die Zehner, dann die Einer. Die schriftlichen Verfahren mit Übertrag kommen danach."},
        {"q": "Wie übt man den Zehnerübergang?", "a": "Erst bis zum nächsten Zehner rechnen und dann den Rest. Bei 386 + 7 also 386 + 4 = 390 und 390 + 3 = 393."},
        {"q": "Was ist eine Umkehraufgabe?", "a": "Die Aufgabe, die das Ergebnis zurückrechnet: Zu 500 − 120 = 380 gehört 380 + 120 = 500."},
        {"q": "Wie viel Kopfrechnen ist in Klasse 3 wichtig?", "a": "Sehr wichtig: Aufgaben mit Hunderter- und Zehnerzahlen und kleine Übergänge sollten Kinder im Kopf lösen können."},
    ]
    make_unit(R, "plus-und-minus-bis-1000", "Z",
              "Die Schülerinnen und Schüler addieren und subtrahieren im Zahlenraum bis 1000 im Kopf und halbschriftlich, nutzen Rechenstrategien und kontrollieren mit der Umkehraufgabe (Zusammenfassung).",
              "Plus und Minus bis 1000: Kopfrechnen und halbschriftlich",
              "Plus und Minus bis 1000 – Mathe Klasse 3 Arbeitsblätter mit Lösungen",
              "Plus und Minus bis 1000",
              "Mathe Klasse 3: Addition und Subtraktion bis 1000 im Kopf und halbschriftlich, Zehner- und Hunderterübergang, Ergänzen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Erst die Hunderter, dann die Zehner, dann die Einer.",
              "Mit der Umkehraufgabe kannst du jedes Ergebnis prüfen.",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
