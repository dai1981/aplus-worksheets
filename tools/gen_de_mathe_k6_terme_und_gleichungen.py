# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Terme und Gleichungen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k6_terme_und_gleichungen.py
Gleichartige Terme zusammenfassen, Klammern auflösen (Distributivgesetz), Termwerte mit Brüchen und Dezimalzahlen, Gleichungen mit Umkehroperationen und Waagemodell lösen, Gleichungen aufstellen.
Fehler: 3x + 2 = 5x, 3(x + 2) = 3x + 2, auf einer Seite der Gleichung anders umgeformt als auf der anderen.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz, mcq as _mcq

R = random.Random(49614)
KIDS = Kids(R)
G = ":"


def mcq(q, a, c, e):
    return _mcq(q, a, c, e, neg=True)


def t(k, v):
    """Koeffizient und Variable: 1x → x"""
    if k == 1:
        return v
    if k == -1:
        return "−" + v
    return "%s%s" % (("−%d" % -k) if k < 0 else str(k), v)


def summe(parts):
    out = ""
    for i, (k, v) in enumerate(parts):
        if k == 0:
            continue
        s = t(abs(k), v) if v else str(abs(k))
        if not out:
            out = ("−" if k < 0 else "") + s
        else:
            out += (" − " if k < 0 else " + ") + s
    return out or "0"


def zusammen():
    kind = R.choice(["eine", "zwei", "zwei"])
    if kind == "eine":
        a, b = R.randint(2, 12), R.randint(1, 9)
        op = R.choice([1, -1])
        if op < 0 and a == b:
            return None
        v = a + op * b
        q = summe([(a, "x"), (op * b, "x")])
        return mcq("Fasse zusammen: %s" % q, summe([(v, "x")]), [summe([(a * b, "x")]) if op > 0 else summe([(a + b, "x")]), summe([(v, "x²")]) if op > 0 else summe([(-v, "x")]), summe([(v + 1, "x")])],
                   "Gleichartige Terme: %d %s %d = %s. <b>%s</b>" % (a, "+" if op > 0 else "−", b, dz(v), summe([(v, "x")])))
    a, b, c, d = R.randint(2, 9), R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
    v1, v2 = R.sample(["a", "b", "x", "y"], 2)
    q = summe([(a, v1), (b, v2), (c, v1), (d, v2)])
    ans = summe([(a + c, v1), (b + d, v2)])
    return mcq("Fasse zusammen: %s" % q, ans, [summe([(a + b + c + d, v1 + v2)]), summe([(a + b, v1), (c + d, v2)]), summe([(a + c + b + d, v1)])],
               "Nur gleiche Variablen zusammenfassen: %s und %s. <b>%s</b>" % (summe([(a, v1), (c, v1)]), summe([(b, v2), (d, v2)]), ans))


def klammer():
    a, b, c = R.randint(2, 9), R.randint(1, 9), R.randint(1, 9)
    kind = R.choice(["plus", "minus", "zusammen"])
    if kind == "plus":
        return mcq("Löse die Klammer auf: %d %s (x + %d)" % (a, MAL, b), "%dx + %d" % (a, a * b), ["%dx + %d" % (a, b), "x + %d" % (a * b), "%dx" % (a + a * b)],
                   "Jeder Summand wird mit %d multipliziert: %d %s x + %d %s %d = <b>%dx + %d</b>." % (a, a, MAL, a, MAL, b, a, a * b))
    if kind == "minus":
        return mcq("Löse die Klammer auf: %d %s (%dx − %d)" % (a, MAL, b, c), "%sx − %d" % (a * b, a * c) if a * b != 1 else "x − %d" % (a * c), ["%dx − %d" % (a * b, c), "%dx − %d" % (a + b, a * c), "%dx + %d" % (a * b, a * c)],
                   "%d %s %dx = %dx, %d %s %d = %d. <b>%dx − %d</b>" % (a, MAL, b, a * b, a, MAL, c, a * c, a * b, a * c))
    v = a * b + c
    return mcq("Vereinfache: %d %s (x + %d) + %dx" % (a, MAL, b, c), "%dx + %d" % (a + c, a * b), ["%dx + %d" % (a + c, b), "%dx + %d" % (a, a * b + c), "%dx" % (a + c + a * b)],
               "Klammer auflösen: %dx + %d + %dx. Zusammenfassen: <b>%dx + %d</b>." % (a, a * b, c, a + c, a * b))


def wert():
    kind = R.choice(["dez", "neg", "zwei"])
    if kind == "dez":
        x = Fr(R.randint(1, 30), 10)
        a, b = R.randint(2, 9), R.randint(1, 20)
        v = a * x + b
        return mcq("Berechne %dx + %d für x = %s." % (a, b, dz(x)), dz(v), [dz(a + x + b), dz(a * (x + b)), dz(v + a)],
                   "%d %s %s + %d = %s + %d = <b>%s</b>." % (a, MAL, dz(x), b, dz(a * x), b, dz(v)))
    if kind == "neg":
        x = R.randint(-9, -1)
        a, b = R.randint(2, 9), R.randint(1, 20)
        v = a * x + b
        return mcq("Berechne %dx + %d für x = %s." % (a, b, dz(x)), dz(v), [dz(-a * x + b), dz(a + x + b), dz(a * x - b)],
                   "%d %s (%s) + %d = %s + %d = <b>%s</b>." % (a, MAL, dz(x), b, dz(a * x), b, dz(v)))
    x, y = R.randint(1, 9), R.randint(1, 9)
    a, b = R.randint(2, 6), R.randint(2, 6)
    v = a * x - b * y
    return mcq("Berechne %da − %db für a = %d und b = %d." % (a, b, x, y), dz(v), [dz(a * y - b * x) if a * y - b * x != v else dz(v + 1), dz(a + x - b - y), dz(-v) if v else "1"],
               "%d %s %d − %d %s %d = %d − %d = <b>%s</b>." % (a, MAL, x, b, MAL, y, a * x, b * y, dz(v)))


def gleichung():
    x = R.randint(-10, 15)
    kind = R.choice(["ax+b", "ax-b", "ax+b", "beide"])
    a, b = R.randint(2, 9), R.randint(1, 30)
    if kind == "ax+b":
        r = a * x + b
        return mcq("Löse die Gleichung: %dx + %d = %s" % (a, b, dz(r)), "x = %s" % dz(x), ["x = %s" % dz(Fr(r + b, a)) if (r + b) % a == 0 else "x = %s" % dz(r - b), "x = %s" % dz(r - b - a), "x = %s" % dz(-x) if x else "x = 1"],
                   "Auf beiden Seiten − %d: %dx = %s. Auf beiden Seiten : %d: <b>x = %s</b>." % (b, a, dz(r - b), a, dz(x)))
    if kind == "ax-b":
        r = a * x - b
        return mcq("Löse die Gleichung: %dx − %d = %s" % (a, b, dz(r)), "x = %s" % dz(x), ["x = %s" % dz(Fr(r - b, a)) if (r - b) % a == 0 else "x = %s" % dz(r + b), "x = %s" % dz(-x) if x else "x = 2", "x = %s" % dz(x + 1)],
                   "Auf beiden Seiten + %d: %dx = %s. Auf beiden Seiten : %d: <b>x = %s</b>." % (b, a, dz(r + b), a, dz(x)))
    c = R.randint(1, a - 1) if a > 2 else None
    if c is None:
        return None
    d = (a - c) * x + b
    return mcq("Löse die Gleichung: %dx + %d = %dx + %s" % (a, b, c, dz(d)) if d >= 0 else "Löse die Gleichung: %dx + %d = %dx − %s" % (a, b, c, dz(-d)), "x = %s" % dz(x),
               ["x = %s" % dz(Fr(d - b, a + c)) if Fr(d - b, a + c).denominator in (1, 2, 5, 10) else "x = %s" % dz(x + 2), "x = %s" % dz(d - b), "x = %s" % dz(-x) if x else "x = 1"],
               "Auf beiden Seiten − %dx: %dx + %d = %s. Dann − %d und : %d: <b>x = %s</b>." % (c, a - c, b, dz(d), b, a - c, dz(x)))


def aufstellen():
    p, er = KIDS.next()
    kind = R.choice(["zahl", "alter", "umfang", "geld", "zahl2"])
    if kind == "zahl":
        a, b = R.randint(2, 7), R.randint(3, 20)
        x = R.randint(2, 15)
        r = a * x + b
        return mcq("Das %d-Fache einer Zahl, vermehrt um %d, ergibt %d. Wie heißt die Zahl?" % (a, b, r), str(x), [str(Fr(r + b, a)) if (r + b) % a == 0 else str(r - b), str(r - b), str(x + 1)],
                   "Gleichung: %dx + %d = %d. %dx = %d, <b>x = %d</b>." % (a, b, r, a, r - b, x))
    if kind == "alter":
        x = R.randint(8, 14)
        d = R.randint(20, 35)
        s = 2 * x + d
        return mcq("%s und die Mutter sind zusammen %d Jahre alt. Die Mutter ist %d Jahre älter als %s. Wie alt ist %s?" % (p, s, d, p, p), "%d Jahre" % x, ["%d Jahre" % v for v in (s - d, x + d, s // 2)],
                   "x + (x + %d) = %d. 2x = %d, <b>x = %d</b>." % (d, s, s - d, x))
    if kind == "umfang":
        b = R.randint(3, 12)
        a = b + R.randint(2, 10)
        u = 2 * (a + b)
        return mcq("Ein Rechteck ist %d cm länger als breit. Der Umfang ist %d cm. Wie breit ist es?" % (a - b, u), "%d cm" % b, ["%d cm" % v for v in (a, u // 4, (u - (a - b)) // 2)],
                   "2 %s (x + x + %d) = %d. 2x + %d = %d, 2x = %d, <b>x = %d</b>." % (MAL, a - b, u, a - b, u // 2, 2 * b, b))
    if kind == "geld":
        g = R.choice([5, 8, 10])
        k = R.randint(3, 9)
        pr = R.choice([2, 3, 4])
        t_ = g + k * pr
        return mcq("Ein Eintritt kostet %d €, jede Fahrt kostet %d €. %s bezahlt insgesamt %d €. Wie viele Fahrten hat %s gemacht?" % (g, pr, p, t_, er), str(k), [str(t_ // pr), str(t_ - g), str(k + 1)],
                   "%d + %dx = %d. %dx = %d, <b>x = %d</b>." % (g, pr, t_, pr, t_ - g, k))
    x = R.randint(3, 20)
    a = R.randint(2, 5)
    return mcq("Wenn man von einer Zahl %d subtrahiert und das Ergebnis mit %d multipliziert, erhält man %d. Wie heißt die Zahl?" % (a, a, a * (x - a)), str(x) if x - a > 0 else None, [str(x - a), str(a * (x - a) + a), str(x + a)],
               "(x − %d) %s %d = %d. x − %d = %d, <b>x = %d</b>." % (a, MAL, a, a * (x - a), a, x - a, x)) if x - a > 0 else None


def main():
    seen = set()
    sets = [
        ("Terme zusammenfassen", mix(R, seen, [(zusammen, 20)])),
        ("Klammern auflösen", mix(R, seen, [(klammer, 20)])),
        ("Termwerte berechnen", mix(R, seen, [(wert, 20)])),
        ("Gleichungen lösen", mix(R, seen, [(gleichung, 20)])),
        ("Gleichungen aufstellen", mix(R, seen, [(aufstellen, 20)])),
    ]
    body = lesson(
        ["<b>Gleichartige Terme</b> (gleiche Variable) darf man zusammenfassen: 3x + 5x = 8x. 3x + 2 bleibt 3x + 2.",
         "<b>Klammern auflösen</b>: Jeder Summand in der Klammer wird multipliziert: 4 %s (x + 3) = 4x + 12." % MAL,
         "Eine <b>Gleichung</b> ist wie eine Waage: Was man auf einer Seite tut, muss man auch auf der anderen tun.",
         "Ziel: x allein auf eine Seite bringen. Zum Schluss die Probe machen."],
        [example("5x + 7 = 32", ["− 7: 5x = 25", ": 5: x = 5", "Probe: 5 %s 5 + 7 = 32" % MAL], "x = 5"),
         example("3 %s (x + 4) + 2x" % MAL, ["3x + 12 + 2x"], "5x + 12")],
        [["3x + 2 = 5x", "3x und 2 sind nicht gleichartig: 3x + 2"],
         ["4 %s (x + 3) = 4x + 3" % MAL, "Auch die 3 mal 4: 4x + 12"],
         ["5x + 7 = 32, also 5x = 39", "Auf beiden Seiten minus 7: 5x = 25"]])
    faq = [
        {"q": "Welche Terme darf man zusammenfassen?", "a": "Nur Terme mit derselben Variable (oder nur Zahlen): 2a + 3a = 5a, aber 2a + 3b bleibt so."},
        {"q": "Wie löst man eine Gleichung?", "a": "Mit Umkehroperationen auf beiden Seiten, bis x allein steht. Dann setzt man das Ergebnis zur Probe ein."},
        {"q": "Wie löst man eine Klammer auf?", "a": "Den Faktor vor der Klammer mit jedem Summanden in der Klammer multiplizieren."},
        {"q": "Was bedeutet das Waagemodell?", "a": "Eine Gleichung ist im Gleichgewicht. Man darf auf beiden Seiten dasselbe addieren, subtrahieren, multiplizieren oder dividieren."},
    ]
    make_unit(R, "terme-und-gleichungen", "F",
              "Die Schülerinnen und Schüler fassen Terme zusammen, lösen Klammern auf, berechnen Termwerte und lösen Gleichungen mit Umkehroperationen; sie stellen Gleichungen zu Sachsituationen auf (Zusammenfassung).",
              "Terme und Gleichungen",
              "Terme und Gleichungen Klasse 6 – Arbeitsblätter mit Lösungen",
              "Terme & Gleichungen",
              "Terme und Gleichungen für Klasse 6: zusammenfassen, Klammern auflösen, Termwerte, Gleichungen lösen und aufstellen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Was du auf einer Seite tust, tust du auch auf der anderen.",
              "Nur gleichartige Terme zusammenfassen.",
              body, faq, sets, 14, grade="klasse-6")


if __name__ == "__main__":
    main()
