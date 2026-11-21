# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Natürliche Zahlen und Stellenwerte（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_natuerliche_zahlen_und_stellenwerte.py
Stellenwerte bis zu den Milliarden, große Zahlen lesen und schreiben, vergleichen und ordnen, Zahlenstrahl, römische Zahlen.
Fehler: Nullen vergessen (3 Mio. 40 Tsd. = 340 000), Stellen falsch gezählt, römisch IV als 6 gelesen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, table, zahlenstrahl

R = random.Random(49501)
STUFEN = [(10 ** 9, "Milliarden", "Milliarde"), (10 ** 6, "Millionen", "Million"), (10 ** 3, "Tausend", "Tausend")]
STELLE = {0: "Einer", 1: "Zehner", 2: "Hunderter", 3: "Tausender", 4: "Zehntausender", 5: "Hunderttausender",
          6: "Millionen", 7: "Zehnmillionen", 8: "Hundertmillionen", 9: "Milliarden"}


def gemischt(n):
    """3 450 000 → 3 Millionen 450 Tausend"""
    parts = []
    for v, pl, sg in STUFEN:
        q, n = divmod(n, v)
        if q:
            parts.append("%s %s" % (num(q), sg if q == 1 and v > 1000 else pl))
    if n:
        parts.append(num(n))
    return " ".join(parts)


def stellenwert():
    digits = R.randint(6, 10)
    n = R.randint(10 ** (digits - 1), 10 ** digits - 1)
    s = str(n)
    pos = R.randrange(digits)
    d = int(s[digits - 1 - pos])
    if d == 0:
        return None
    if R.random() < 0.5:
        ans = num(d * 10 ** pos)
        w = [num(d * 10 ** (pos + 1)), num(d * 10 ** max(pos - 1, 0)) if pos else num(d * 100), str(d)]
        return mcq("Welchen Wert hat die Ziffer %d an der %s-Stelle von %s?" % (d, STELLE[pos], num(n)), ans, [x for x in w if x != ans],
                   "Die %s-Stelle hat den Wert %s. %d %s %s = <b>%s</b>." % (STELLE[pos], num(10 ** pos), d, "·", num(10 ** pos), ans))
    ans = STELLE[pos]
    w = [STELLE[p] for p in (pos + 1, pos - 1, pos + 2) if 0 <= p <= 9]
    if s.count(str(d)) != 1:
        return None
    return mcq("An welcher Stelle steht die Ziffer %d in %s?" % (d, num(n)), ans, w,
               "Zähle von rechts: Einer, Zehner, Hunderter … Die %d steht an der <b>%s</b>-Stelle." % (d, ans))


def lesen():
    kind = R.choice(["zahl", "wort", "zerlegt"])
    st = R.choice([10 ** 6, 10 ** 9])
    a = R.randint(2, 99)
    b = R.choice([R.randint(1, 999), R.randint(1, 99) * 10, R.randint(1, 9) * 100])
    n = a * st + b * (st // 1000)
    if kind == "zahl":
        txt = gemischt(n)
        w = [num(a * st + b * (st // 10 ** 6) if st == 10 ** 9 else a * st + b), num(a * st // 10 + b * (st // 1000)), num(a * st * 10 + b * (st // 1000))]
        return mcq("Schreibe als Zahl: %s" % txt, num(n), [x for x in w if x != num(n)],
                   "Fülle die Stellen mit Nullen auf: <b>%s</b>." % num(n))
    if kind == "wort":
        return mcq("Wie liest man %s?" % num(n), gemischt(n), [gemischt(a * st // 1000 + b * (st // 10 ** 6)) if st == 10 ** 9 else gemischt(a * 1000 + b),
                                                              gemischt(a * st * 10 + b * (st // 1000)), gemischt(b * st + a * (st // 1000)) if b < 1000 else gemischt(n + st)],
                   "Teile in Dreiergruppen von rechts: <b>%s</b>." % gemischt(n))
    z = R.randint(1, 9)
    m = z * st + b * (st // 1000) + R.randint(1, 9)
    parts = [(z * st, None), (b * (st // 1000), None)]
    rest = m - z * st - b * (st // 1000)
    return mcq("%s + %s + %s = ?" % (num(z * st), num(b * (st // 1000)), num(rest)), num(m),
               [num(z * st + b * (st // 10 ** 6) + rest) if st == 10 ** 9 else num(z * st + b + rest), num(z * st // 10 + b * (st // 1000) + rest), num(m + st)],
               "Jede Zahl an ihre Stelle: <b>%s</b>." % num(m))


def vergleichen():
    kind = R.choice(["groesser", "ordnen", "naechste"])
    if kind == "groesser":
        d = R.randint(7, 10)
        a = R.randint(10 ** (d - 1), 10 ** d - 1)
        b = int(str(a)[:R.randint(2, d - 1)] + "".join(str(R.randint(0, 9)) for _ in range(d - len(str(a)[:R.randint(2, d - 1)]))))
        b = int(str(b)[:d].ljust(d, "0"))
        if a == b:
            return None
        big = max(a, b)
        return mcq("Welche Zahl ist größer: %s oder %s?" % (num(a), num(b)), num(big), [num(min(a, b)), "Beide sind gleich groß", "Das kann man nicht sagen"],
                   "Vergleiche Stelle für Stelle von links. Größer ist <b>%s</b>." % num(big))
    if kind == "ordnen":
        base = R.randint(10, 99) * 10 ** 6
        nums = list({base + R.randint(0, 9) * 10 ** R.randint(3, 6) + R.randint(0, 999) for _ in range(4)})
        if len(nums) < 4:
            return None
        s = sorted(nums)
        ans = " &lt; ".join(num(x) for x in s)
        return mcq("Ordne der Größe nach, beginne mit der kleinsten Zahl.", ans,
                   [" &lt; ".join(num(x) for x in s[::-1]), " &lt; ".join(num(x) for x in [s[1], s[0], s[2], s[3]]), " &lt; ".join(num(x) for x in [s[0], s[1], s[3], s[2]])],
                   "Gleiche Millionen, also die nächsten Stellen vergleichen: <b>%s</b>." % ans)
    n = R.randint(10 ** 6, 10 ** 9)
    kind2 = R.choice(["vor", "nach"])
    if kind2 == "vor":
        return mcq("Welche Zahl kommt direkt vor %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 1000)], "Eins weniger: <b>%s</b>." % num(n - 1))
    return mcq("Welche Zahl kommt direkt nach %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 1000)], "Eins mehr: <b>%s</b>." % num(n + 1))


def strahl():
    step = R.choice([10 ** 5, 10 ** 6, 5 * 10 ** 5, 2 * 10 ** 6])
    lo = R.randint(0, 5) * step * 10
    k = R.randint(1, 9)
    v = lo + k * step
    pic = zahlenstrahl(lo, lo + 10 * step, step, marks=[(v, "A")], every=5 * step, label="Zahlenstrahl")
    return mcq(pic + "Welche Zahl gehört zum Pfeil A?", num(v), [num(lo + k * step * 10) if lo + k * step * 10 != v else num(v + step), num(v + step), num(v - step)],
               "Ein Strich bedeutet %s. Von %s aus %d Striche: <b>%s</b>." % (num(step), num(lo), k, num(v)))


ROM = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def roman(n):
    s = ""
    for v, r in ROM:
        while n >= v:
            s += r
            n -= v
    return s


def naiv(r):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    return sum(vals[c] for c in r)


def roemisch():
    n = R.choice([R.randint(4, 49), R.randint(50, 499), R.randint(500, 2026)])
    r = roman(n)
    if R.random() < 0.5:
        w = [naiv(r) if naiv(r) != n else n + 2, n + 10, n - 1]
        return mcq("Welche Zahl ist %s?" % r, num(n), [num(x) for x in w if x != n] + [num(n + 5)],
                   ("Steht ein kleineres Zeichen vor einem größeren, wird es abgezogen: %s = <b>%s</b>." if naiv(r) != n else "Addiere die Werte der Zeichen: %s = <b>%s</b>.") % (r, num(n)))
    alt = r.replace("IV", "IIII").replace("IX", "VIIII").replace("XL", "XXXX").replace("XC", "LXXXX").replace("CD", "CCCC").replace("CM", "DCCCC")
    w = [alt if alt != r else roman(n + 1), roman(n + 10), roman(n - 1) if n > 1 else roman(n + 2)]
    return mcq("Wie schreibt man %s mit römischen Zahlzeichen?" % num(n), r, [x for x in dict.fromkeys(w) if x != r] + [roman(n + 5)],
               "<b>%s</b>. Dasselbe Zeichen steht höchstens dreimal hintereinander." % r)


def main():
    seen = set()
    sets = [
        ("Stellenwerte", mix(R, seen, [(stellenwert, 20)])),
        ("Große Zahlen lesen und schreiben", mix(R, seen, [(lesen, 20)])),
        ("Vergleichen und ordnen", mix(R, seen, [(vergleichen, 20)])),
        ("Am Zahlenstrahl", mix(R, seen, [(strahl, 20)])),
        ("Römische Zahlen", mix(R, seen, [(roemisch, 20)])),
    ]
    body = lesson(
        ["Unser Zahlsystem ist ein <b>Zehnersystem</b>: 10 Einer sind 1 Zehner, 10 Zehner sind 1 Hunderter usw.",
         "Große Zahlen liest man in <b>Dreiergruppen</b> von rechts: Tausend, Million, Milliarde. 1 Million = 1 000 000, 1 Milliarde = 1 000 000 000.",
         "Beim Vergleichen zählst du zuerst die Stellen. Haben beide gleich viele Stellen, vergleichst du von links.",
         "Römische Zahlen: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. Steht ein kleineres Zeichen vor einem größeren, wird es abgezogen (IV = 4)."],
        [example("3 Millionen 40 Tausend", ["3 000 000 + 40 000"], "3 040 000"),
         example("MCMXCIV", ["M = 1000, CM = 900, XC = 90, IV = 4"], "1994")],
        [["3 Millionen 40 Tausend = 340 000", "Nullen auffüllen: 3 040 000"],
         ["Längere Zahl ist nicht immer erkannt", "Erst die Anzahl der Stellen vergleichen"],
         ["IV = 6", "IV = 5 − 1 = 4"]],
        extra=table(["Name", "Zahl"], [["eine Million", "1 000 000"], ["eine Milliarde", "1 000 000 000"], ["eine Billion", "1 000 000 000 000"]]))
    faq = [
        {"q": "Wie viele Nullen hat eine Milliarde?", "a": "Neun: 1 000 000 000. Eine Million hat sechs Nullen, eine Billion zwölf."},
        {"q": "Warum schreibt man große Zahlen mit Leerzeichen?", "a": "In Dreiergruppen sind große Zahlen leichter zu lesen. In Deutschland nutzt man dafür ein kleines Leerzeichen oder einen Punkt."},
        {"q": "Warum lernt man römische Zahlen?", "a": "Sie zeigen, dass es auch andere Zahlsysteme gibt. Man findet sie noch heute auf Uhren, in Büchern und an Gebäuden."},
        {"q": "Was ist ein Stellenwertsystem?", "a": "Der Wert einer Ziffer hängt von ihrer Stelle ab: Die 3 in 300 ist dreihundert, in 30 nur dreißig."},
    ]
    make_unit(R, "natuerliche-zahlen-und-stellenwerte", "Z",
              "Die Schülerinnen und Schüler lesen, schreiben und ordnen große natürliche Zahlen im Zehnersystem, stellen sie am Zahlenstrahl dar und vergleichen das Zehnersystem mit dem römischen Zahlsystem (Zusammenfassung).",
              "Natürliche Zahlen und Stellenwerte",
              "Große Zahlen und Stellenwerte Klasse 5 – Arbeitsblätter mit Lösungen",
              "Große Zahlen",
              "Natürliche Zahlen für Klasse 5: Stellenwerte bis Milliarden, große Zahlen lesen und schreiben, vergleichen, Zahlenstrahl und römische Zahlen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Große Zahlen in Dreiergruppen lesen.",
              "1 Million = 1 000 000, 1 Milliarde = 1 000 000 000",
              body, faq, sets, 1, grade="klasse-5")


if __name__ == "__main__":
    main()
