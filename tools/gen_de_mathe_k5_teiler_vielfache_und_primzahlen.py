# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Teiler, Vielfache und Primzahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_teiler_vielfache_und_primzahlen.py
Teiler und Teilermengen, Vielfache, Teilbarkeitsregeln (2, 3, 4, 5, 9, 10), Primzahlen und Primfaktorzerlegung, ggT und kgV in Sachaufgaben.
Fehler: 1 und die Zahl selbst als Teiler vergessen, 1 als Primzahl gezählt, Quersummenregel bei 4 benutzt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, MAL, table

R = random.Random(49508)


def teiler(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def prim(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def qs(n):
    return sum(int(c) for c in str(n))


def tm():
    n = R.choice([12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72, 75, 80, 84, 90, 96, 100])
    kind = R.choice(["menge", "anzahl", "ist", "nicht"])
    T = teiler(n)
    if kind == "menge":
        ans = "{%s}" % ", ".join(map(str, T))
        w = ["{%s}" % ", ".join(map(str, T[1:-1])), "{%s}" % ", ".join(map(str, T[:-1])), "{%s}" % ", ".join(map(str, [t for t in T if t != T[len(T) // 2]]))]
        return mcq("Welche Menge enthält alle Teiler von %d?" % n, ans, w, "Teiler finden in Paaren: %s. <b>%s</b>" % (", ".join("%d %s %d" % (d, MAL, n // d) for d in T if d * d <= n), ans))
    if kind == "anzahl":
        k = len(T)
        return mcq("Wie viele Teiler hat %d?" % n, str(k), [str(k - 2), str(k - 1), str(k + 1)], "T(%d) = {%s}: <b>%d</b> Teiler." % (n, ", ".join(map(str, T)), k))
    if kind == "ist":
        d = R.choice([t for t in T if 1 < t < n])
        bad = [x for x in range(2, n) if n % x][:20]
        bs = R.sample(bad, 3)
        return mcq("Welche dieser Zahlen ist ein Teiler von %d: %s?" % (n, ", ".join(str(x) for x in sorted(bs + [d]))), str(d), [str(x) for x in bs], "%d %s %d = %d: <b>%d</b> ist ein Teiler." % (d, MAL, n // d, n, d))
    bad = R.choice([x for x in range(2, n) if n % x])
    good = R.sample([t for t in T if t != bad], 3)
    return mcq("Welche Zahl ist <b>kein</b> Teiler von %d?" % n, str(bad), [str(x) for x in good], "%d : %d geht nicht ohne Rest auf: <b>%d</b>." % (n, bad, bad))


def vielfache():
    k = R.randint(3, 15)
    kind = R.choice(["liste", "ist", "naechstes", "gemeinsam"])
    if kind == "liste":
        ans = ", ".join(str(k * i) for i in range(1, 6))
        return mcq("Welche Zahlen sind die ersten fünf Vielfachen von %d?" % k, ans,
                   [", ".join(str(k + i) for i in range(5)), ", ".join(str(k * i) for i in range(2, 7)), ", ".join(str(d) for d in teiler(k * 4)[:5])],
                   "%d, 2 %s %d, 3 %s %d … <b>%s</b>." % (k, MAL, k, MAL, k, ans))
    if kind == "ist":
        good = k * R.randint(6, 15)
        bads = [good + R.choice([-1, 1, 2]), good + k // 2 if k > 2 else good + 1, good - k + 1]
        return mcq("Welche dieser Zahlen ist ein Vielfaches von %d: %s?" % (k, ", ".join(str(x) for x in sorted(bads + [good]))), str(good), [str(b) for b in bads], "%d = %d %s %d: <b>%d</b>." % (good, good // k, MAL, k, good))
    if kind == "naechstes":
        x = R.randint(30, 200)
        r = (x // k + 1) * k
        return mcq("Welches ist das kleinste Vielfache von %d, das größer als %d ist?" % (k, x), str(r), [str(r - k) if r - k > x else str(r + k), str(r + k), str(x + 1)],
                   "%d %s %d = %d: <b>%d</b>." % (r // k, MAL, k, r, r))
    a, b = R.sample([2, 3, 4, 5, 6, 8, 9, 10, 12], 2)
    from math import gcd
    l = a * b // gcd(a, b)
    return mcq("Welches ist das kleinste gemeinsame Vielfache (kgV) von %d und %d?" % (a, b), str(l), [str(a * b) if a * b != l else str(l * 2), str(gcd(a, b)) if gcd(a, b) > 1 else str(a + b), str(l + a)],
               "Vielfache von %d: %s … Vielfache von %d: %s … Das erste gemeinsame: <b>%d</b>." % (a, ", ".join(str(a * i) for i in range(1, 5)), b, ", ".join(str(b * i) for i in range(1, 5)), l))


REGELN = {2: "die letzte Ziffer gerade ist", 3: "die Quersumme durch 3 teilbar ist", 4: "die letzten zwei Ziffern eine durch 4 teilbare Zahl bilden",
          5: "die letzte Ziffer 0 oder 5 ist", 9: "die Quersumme durch 9 teilbar ist", 10: "die letzte Ziffer 0 ist"}


def regeln():
    d = R.choice(list(REGELN))
    good = d * R.randint(120, 9999 // d)
    if R.random() < 0.5:
        bads = []
        while len(bads) < 3:
            x = R.randint(1000, 9999)
            if x % d and x not in bads:
                if d == 4 and x % 2 == 0:
                    bads.insert(0, x)
                elif d == 9 and x % 3 == 0:
                    bads.insert(0, x)
                else:
                    bads.append(x)
        bads = bads[:3]
        alle = sorted(bads + [good])
        return mcq("Welche dieser Zahlen ist durch %d teilbar: %s?" % (d, ", ".join(num(x) for x in alle)), num(good), [num(b) for b in bads],
                   "Eine Zahl ist durch %d teilbar, wenn %s. %s%s" % (d, REGELN[d], ("Quersumme von %s: %d. " % (num(good), qs(good))) if d in (3, 9) else "", "<b>%s</b>." % num(good)))
    items = [("Woran erkennst du, ob eine Zahl durch 3 teilbar ist?", "An der Quersumme", ["An der letzten Ziffer", "An den letzten zwei Ziffern", "An der ersten Ziffer"]),
             ("Woran erkennst du, ob eine Zahl durch 4 teilbar ist?", "An den letzten zwei Ziffern", ["An der Quersumme", "An der letzten Ziffer allein", "An der ersten Ziffer"]),
             ("Woran erkennst du, ob eine Zahl durch 5 teilbar ist?", "Die letzte Ziffer ist 0 oder 5.", ["Die Quersumme ist 5.", "Die erste Ziffer ist 5.", "Die Zahl ist ungerade."]),
             ("Ist jede durch 9 teilbare Zahl auch durch 3 teilbar?", "Ja, denn 9 = 3 %s 3." % MAL, ["Nein, nie.", "Nur gerade Zahlen.", "Nur Zahlen mit 9 am Ende."]),
             ("Ist jede durch 3 teilbare Zahl auch durch 9 teilbar?", "Nein, zum Beispiel 12.", ["Ja, immer.", "Ja, wenn sie gerade ist.", "Nein, keine einzige."])]
    q, a, w = R.choice(items)
    return mcq(q, a, w, "<b>%s</b>" % a)


def primzahlen():
    kind = R.choice(["ist", "nicht", "zerlegung", "zerlegung", "zaehlen"])
    P = [n for n in range(2, 100) if prim(n)]
    if kind == "ist":
        good = R.choice(P[3:])
        bads = R.sample([n for n in range(9, 100) if not prim(n) and n % 2 == 1] + [1], 3)
        return mcq("Welche dieser Zahlen ist eine Primzahl: %s?" % ", ".join(str(x) for x in sorted(bads + [good])), str(good), [str(b) for b in bads],
                   "Eine Primzahl hat genau zwei Teiler: 1 und sich selbst. <b>%d</b> ist eine Primzahl." % good)
    if kind == "nicht":
        bad = R.choice([1, 9, 15, 21, 27, 33, 39, 49, 51, 57, 63, 69, 77, 81, 87, 91])
        good = R.sample([p for p in P if p > 3], 3)
        why = "1 hat nur einen Teiler." if bad == 1 else "%d = %d %s %d." % (bad, min(d for d in range(2, bad) if bad % d == 0), MAL, bad // min(d for d in range(2, bad) if bad % d == 0))
        return mcq("Welche dieser Zahlen ist <b>keine</b> Primzahl: %s?" % ", ".join(str(x) for x in sorted(good + [bad])), str(bad), [str(g) for g in good], "%s <b>%d</b> ist keine Primzahl." % (why, bad))
    if kind == "zaehlen":
        lo = R.choice([1, 11, 21, 31, 41, 51, 61, 71, 81, 91])
        ps = [n for n in range(lo, lo + 10) if prim(n)]
        return mcq("Wie viele Primzahlen liegen zwischen %d und %d?" % (lo - 1, lo + 10) if lo > 1 else "Wie viele Primzahlen gibt es von 1 bis 10?", str(len(ps)),
                   [str(len(ps) + 1), str(len(ps) - 1) if len(ps) else "2", str(len(ps) + 2)], "Es sind %s: <b>%d</b>." % (", ".join(map(str, ps)) or "keine", len(ps)))
    n = R.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 72, 75, 84, 90, 96, 98, 100, 120, 126, 150])
    fs, m, d = [], n, 2
    while m > 1:
        while m % d == 0:
            fs.append(d)
            m //= d
        d += 1
    ans = (" %s " % MAL).join(map(str, fs))
    w = []
    for a in range(2, n):
        if n % a == 0 and not prim(a):
            w.append("%d %s %d" % (a, MAL, n // a))
            break
    w.append((" %s " % MAL).join(map(str, fs[:-1] + [fs[-1] + 1])))
    w.append((" %s " % MAL).join(map(str, [1] + fs)))
    return mcq("Zerlege %d in Primfaktoren." % n, ans, w, "Teile immer durch die kleinste Primzahl: <b>%d = %s</b>." % (n, ans))


def sache():
    from math import gcd
    kind = R.choice(["ggt", "kgv", "reihen", "kgv2"])
    if kind == "ggt":
        g = R.choice([4, 5, 6, 8, 10, 12])
        a, b = g * R.randint(2, 7), g * R.randint(2, 7)
        if a == b or gcd(a, b) != g:
            return None
        return mcq("%d Äpfel und %d Birnen sollen so auf Tüten verteilt werden, dass in jeder Tüte gleich viele Äpfel und gleich viele Birnen sind. Wie viele Tüten kann man höchstens packen?" % (a, b),
                   str(g), [str(gcd(a, b) // 2) if g % 2 == 0 else str(g + 1), str(a + b), str(a * b // g)], "Gesucht ist der größte gemeinsame Teiler: ggT(%d, %d) = <b>%d</b>." % (a, b, g))
    if kind == "kgv":
        a, b = R.sample([4, 6, 8, 9, 10, 12, 15], 2)
        l = a * b // gcd(a, b)
        return mcq("Ein Bus fährt alle %d Minuten, ein anderer alle %d Minuten. Um 8:00 Uhr fahren beide gleichzeitig. Nach wie vielen Minuten fahren sie wieder gleichzeitig?" % (a, b),
                   "%d min" % l, ["%d min" % x for x in (a * b if a * b != l else l * 2, a + b, gcd(a, b) if gcd(a, b) > 1 else l + a)], "Gesucht ist das kgV(%d, %d) = <b>%d</b> Minuten." % (a, b, l))
    if kind == "reihen":
        n = R.choice([24, 30, 36, 40, 48, 60])
        k = R.choice([d for d in teiler(n) if 2 < d < n // 2])
        return mcq("%d Stühle sollen in gleich langen Reihen aufgestellt werden. Geht das mit Reihen zu %d Stühlen?" % (n, k), "Ja, %d Reihen." % (n // k),
                   ["Nein, es bleiben Stühle übrig.", "Ja, %d Reihen." % (n // k + 1), "Ja, %d Reihen." % (n - k)], "%d ist ein Teiler von %d: %d : %d = <b>%d Reihen</b>." % (k, n, n, k, n // k))
    a, b = R.sample([3, 4, 5, 6, 8], 2)
    l = a * b // gcd(a, b)
    return mcq("Lina geht alle %d Tage schwimmen, Tom alle %d Tage. Heute waren beide im Bad. In wie vielen Tagen treffen sie sich dort wieder?" % (a, b), "in %d Tagen" % l,
               ["in %d Tagen" % x for x in (a + b, a * b if a * b != l else l + a, max(a, b))], "kgV(%d, %d) = <b>%d</b>." % (a, b, l))


def main():
    seen = set()
    sets = [
        ("Teiler", mix(R, seen, [(tm, 20)])),
        ("Vielfache", mix(R, seen, [(vielfache, 20)])),
        ("Teilbarkeitsregeln", mix(R, seen, [(regeln, 20)])),
        ("Primzahlen und Primfaktoren", mix(R, seen, [(primzahlen, 20)])),
        ("ggT und kgV in Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Eine Zahl t ist ein <b>Teiler</b> von n, wenn n : t ohne Rest aufgeht. 1 und n selbst sind immer Teiler.",
         "<b>Vielfache</b> einer Zahl entstehen, wenn du sie mit 1, 2, 3 … multiplizierst.",
         "Teilbarkeitsregeln: durch 2, 5, 10 an der letzten Ziffer; durch 4 an den letzten zwei Ziffern; durch 3 und 9 an der Quersumme.",
         "Eine <b>Primzahl</b> hat genau zwei Teiler. Die 1 ist keine Primzahl. Jede Zahl lässt sich in Primfaktoren zerlegen: 60 = 2 %s 2 %s 3 %s 5." % (MAL, MAL, MAL)],
        [example("Teiler von 24", ["1 %s 24, 2 %s 12, 3 %s 8, 4 %s 6" % (MAL, MAL, MAL, MAL)], "1, 2, 3, 4, 6, 8, 12, 24"),
         example("Ist 7452 durch 9 teilbar?", ["Quersumme 7 + 4 + 5 + 2 = 18", "18 ist durch 9 teilbar"], "ja")],
        [["1 und die Zahl selbst vergessen", "Teiler in Paaren aufschreiben"],
         ["1 ist eine Primzahl", "1 hat nur einen Teiler, also keine Primzahl"],
         ["Durch 4 teilbar, weil die Quersumme durch 4 teilbar ist", "Bei 4 zählen die letzten zwei Ziffern"]],
        extra=table(["teilbar durch", "Regel"], [[str(k), v[0].upper() + v[1:]] for k, v in REGELN.items()]))
    faq = [
        {"q": "Warum ist 1 keine Primzahl?", "a": "Eine Primzahl hat genau zwei verschiedene Teiler. Die 1 hat nur einen Teiler, nämlich sich selbst."},
        {"q": "Wie findet man alle Teiler einer Zahl?", "a": "Man sucht Teilerpaare: 1 · 36, 2 · 18, 3 · 12, 4 · 9, 6 · 6. Wenn sich die Paare wiederholen, ist man fertig."},
        {"q": "Wozu braucht man ggT und kgV?", "a": "Den ggT zum gerechten Aufteilen und zum Kürzen von Brüchen, das kgV für Fahrpläne und zum Gleichnamigmachen von Brüchen."},
        {"q": "Was ist eine Quersumme?", "a": "Die Summe der Ziffern einer Zahl. Die Quersumme von 7452 ist 7 + 4 + 5 + 2 = 18."},
    ]
    make_unit(R, "teiler-vielfache-und-primzahlen", "Z",
              "Die Schülerinnen und Schüler bestimmen Teiler und Vielfache, nutzen Teilbarkeitsregeln, erkennen Primzahlen, zerlegen Zahlen in Primfaktoren und verwenden ggT und kgV in Sachsituationen (Zusammenfassung).",
              "Teiler, Vielfache und Primzahlen",
              "Teiler, Vielfache und Primzahlen Klasse 5 – Arbeitsblätter mit Lösungen",
              "Teiler und Primzahlen",
              "Teiler, Vielfache und Primzahlen für Klasse 5: Teilermengen, Vielfache, Teilbarkeitsregeln, Primfaktorzerlegung, ggT und kgV. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Primzahl: genau zwei Teiler.",
              "Quersumme durch 3 teilbar → Zahl durch 3 teilbar.",
              body, faq, sets, 8, grade="klasse-5")


if __name__ == "__main__":
    main()
