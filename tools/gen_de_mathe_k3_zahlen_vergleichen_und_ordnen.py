# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Zahlen vergleichen und ordnen（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_zahlen_vergleichen_und_ordnen.py
<, >, =; größte und kleinste Zahl; ordnen; Zahlen dazwischen; größte Zahl aus Ziffern; Sachaufgaben.
Fehler: nur auf die Einer schauen, Zeichen verdreht (das Maul frisst die größere Zahl), längere Zahl ≠ größer bei gleichen Stellen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids

R = random.Random(49002)
KIDS = Kids(R)


def close_pair():
    a = R.randint(101, 989)
    kind = R.choice(["e", "z", "h", "dreh"])
    if kind == "e":
        b = a // 10 * 10 + R.choice([d for d in range(10) if d != a % 10])
    elif kind == "z":
        b = a // 100 * 100 + R.choice([d for d in range(10) if d != a // 10 % 10]) * 10 + a % 10
    elif kind == "h":
        b = R.choice([d for d in range(1, 10) if d != a // 100]) * 100 + a % 100
    else:
        z, e = a // 10 % 10, a % 10
        if z == e:
            return None
        b = a // 100 * 100 + e * 10 + z
    return (a, b) if a != b else None


def s1_zeichen():
    p = close_pair()
    if not p:
        return None
    a, b = p
    sign = "&lt;" if a < b else "&gt;"
    wrong = "&gt;" if sign == "&lt;" else "&lt;"
    ans = "%s %s %s" % (num(a), sign, num(b))
    w = ["%s %s %s" % (num(a), wrong, num(b)), "%s %s %s" % (num(b), sign, num(a)), "%s = %s" % (num(a), num(b))]
    return mcq("Vergleiche %s und %s. Was ist richtig?" % (num(a), num(b)), ans, w,
               "Vergleiche von vorne: erst die Hunderter, dann die Zehner, dann die Einer. Die Spitze zeigt zur kleineren Zahl: <b>%s</b>." % ans)


def s1_luecke():
    p = close_pair()
    if not p:
        return None
    a, b = p
    sign = "&lt;" if a < b else "&gt;"
    q = "Setze richtig ein: %s ☐ %s" % (num(a), num(b))
    return mcq(q, sign, ["&gt;" if sign == "&lt;" else "&lt;", "=", "+"],
               "%s ist %s als %s, also <b>%s %s %s</b>." % (num(a), "kleiner" if a < b else "größer", num(b), num(a), sign, num(b)))


def four_close():
    base = R.randint(1, 8) * 100 + R.randint(0, 9) * 10
    digs = R.sample(range(10), 4)
    kind = R.choice(["e", "dreh", "mix"])
    if kind == "e":
        ns = [base + d for d in digs]
    elif kind == "dreh":
        h = R.randint(1, 9)
        z, e = R.sample(range(1, 10), 2)
        ns = [h * 100 + z * 10 + e, h * 100 + e * 10 + z, z * 100 + h * 10 + e, e * 100 + z * 10 + h]
        if len(set(ns)) < 4:
            return None
    else:
        ns = R.sample(range(base, base + 100), 4)
    return ns


def s2_max():
    ns = four_close()
    if not ns:
        return None
    big = R.choice([True, False])
    ans = max(ns) if big else min(ns)
    sh = ns[:]
    R.shuffle(sh)
    return mcq("Welche Zahl ist am %s? %s" % ("größten" if big else "kleinsten", ", ".join(num(x) for x in sh)), num(ans), [num(x) for x in ns if x != ans],
               "Vergleiche zuerst die Hunderter, dann die Zehner, dann die Einer. Am %s ist <b>%s</b>." % ("größten" if big else "kleinsten", num(ans)))


def s2_ziffern():
    d = R.sample(range(1, 10), 3)
    if R.random() < 0.3:
        d[R.randint(1, 2)] = 0
        if d.count(0) > 1:
            return None
    big = R.choice([True, False])
    s = sorted(d, reverse=big)
    if not big and s[0] == 0:
        s[0], s[1] = s[1], s[0]
    ans = int("".join(map(str, s)))
    w = [int("".join(map(str, sorted(d, reverse=not big)))) if sorted(d, reverse=not big)[0] else None,
         int("".join(map(str, d))), int("".join(map(str, [s[0], s[2], s[1]]))), int("".join(map(str, [s[1], s[0], s[2]]))) if s[1] else None]
    return mcq("Bilde mit den Ziffern %s die %s dreistellige Zahl. Jede Ziffer nur einmal." % (", ".join(map(str, d)), "größte" if big else "kleinste"),
               num(ans), [num(x) for x in w if x and x >= 100 and x != ans],
               ("Die größte Ziffer kommt nach vorne zu den Hundertern: <b>%s</b>." if big else
                "Die kleinste Ziffer (aber nicht die 0) kommt nach vorne: <b>%s</b>.") % num(ans))


def s3_ordnen():
    ns = four_close()
    if not ns:
        return None
    ns = ns[:3] if R.random() < 0.5 else ns
    up = R.choice([True, False])
    srt = sorted(ns, reverse=not up)
    j = lambda xs: (" &lt; " if up else " &gt; ").join(num(x) for x in xs)
    sh = ns[:]
    R.shuffle(sh)
    w = [j(sorted(ns, reverse=up)), j(srt[1:2] + srt[:1] + srt[2:]), j(srt[:-2] + srt[-1:] + srt[-2:-1]), j(sh)]
    return mcq("Ordne die Zahlen %s: %s" % ("der Größe nach, beginne mit der kleinsten" if up else "der Größe nach, beginne mit der größten",
                                           ", ".join(num(x) for x in ns)),
               j(srt), [x for x in w if x != j(srt)],
               "Vergleiche Stelle für Stelle von vorne. Richtig: <b>%s</b>." % j(srt))


def s4_zwischen():
    lo = R.randint(10, 97) * 10
    step = R.choice([10, 10, 100]) if lo % 100 == 0 and lo <= 800 else 10
    hi = lo + step
    if hi > 1000:
        return None
    v = R.randint(lo + 1, hi - 1)
    w = [lo - R.randint(1, 9) if lo > 10 else hi + 5, hi + R.randint(1, 9), (lo // 10 % 10) * 100 + (lo // 100) * 10 + v % 10 if lo >= 100 else lo + step * 2,
         lo + step * 3 if lo + step * 3 < 1000 else lo - 15]
    return mcq("Welche Zahl liegt zwischen %s und %s?" % (num(lo), num(hi)), num(v),
               [num(x) for x in w if x > 0 and not lo < x < hi and x != v],
               "Sie muss größer als %s und kleiner als %s sein: <b>%s</b>." % (num(lo), num(hi), num(v)))


def s4_mitte():
    a = R.randint(1, 49) * 20
    b = a + R.choice([20, 40, 100, 200])
    if b > 1000:
        return None
    m = (a + b) // 2
    w = [m + 10, m - 10, b - a, a + (b - a) // 4 if (b - a) % 4 == 0 else m + 5]
    return mcq("Welche Zahl liegt genau in der Mitte zwischen %s und %s?" % (num(a), num(b)), num(m),
               [num(x) for x in w if x != m and x > 0],
               "Der Abstand ist %s. Die Hälfte davon ist %s. %s + %s = <b>%s</b>." % (num(b - a), num((b - a) // 2), num(a), num((b - a) // 2), num(m)))


def s5_sache():
    kind = R.choice(["punkte", "seiten", "hoehe", "drei"])
    p1, p2 = KIDS.two()
    pr = close_pair()
    if not pr:
        return None
    a, b = pr
    if kind == "punkte":
        q = "%s hat %s Punkte, %s hat %s Punkte. Wer hat mehr Punkte?" % (p1[0], num(a), p2[0], num(b))
        ans = p1[0] if a > b else p2[0]
        oth = p2[0] if a > b else p1[0]
        return mcq(q, ans, [oth, "Beide gleich viele", "Das kann man nicht wissen"],
                   "%s %s %s, also hat <b>%s</b> mehr Punkte." % (num(a), "&gt;" if a > b else "&lt;", num(b), ans))
    if kind == "seiten":
        q = "Das rote Buch hat %s Seiten, das blaue Buch hat %s Seiten. Welches Buch ist dünner?" % (num(a), num(b))
        ans = "das rote Buch" if a < b else "das blaue Buch"
        oth = "das blaue Buch" if a < b else "das rote Buch"
        return mcq(q, ans[0].upper() + ans[1:], [oth[0].upper() + oth[1:], "Beide sind gleich dick", "Das kann man nicht wissen"],
                   "Weniger Seiten heißt dünner: %s %s %s, also <b>%s</b>." % (num(a), "&lt;" if a < b else "&gt;", num(b), ans))
    if kind == "hoehe":
        if a < b:
            a, b = b, a
        q = "In der Bücherei stehen %s Kinderbücher und %s Sachbücher. Wie viele Kinderbücher sind es mehr als Sachbücher?" % (num(a), num(b))
        d = a - b
        return mcq(q, num(d), [num(x) for x in (a + b if a + b < 1000 else d + 100, d + 10, d - 1 if d > 1 else d + 2, a)],
                   "Größere Zahl minus kleinere Zahl: %s − %s = <b>%s</b>." % (num(a), num(b), num(d)))
    a, b, c = sorted(R.sample(range(200, 990), 3))
    names = KIDS.next(), KIDS.next(), KIDS.next()
    if len({n[0] for n in names}) < 3:
        return None
    vals = [a, b, c]
    R.shuffle(vals)
    q = ("Beim Weitwurf-Spiel sammeln drei Kinder Punkte: %s %s, %s %s und %s %s. Wer ist Zweiter?"
         % (names[0][0], num(vals[0]), names[1][0], num(vals[1]), names[2][0], num(vals[2])))
    order = sorted(range(3), key=lambda i: -vals[i])
    ans = names[order[1]][0]
    return mcq(q, ans, [names[order[0]][0], names[order[2]][0], "Alle sind gleich"],
               "Ordne von groß nach klein: %s. Zweiter ist <b>%s</b>." % (" &gt; ".join(num(vals[i]) for i in order), ans))


def main():
    seen = set()
    sets = [
        ("Größer, kleiner oder gleich?", mix(R, seen, [(s1_zeichen, 12), (s1_luecke, 8)])),
        ("Die größte und die kleinste Zahl", mix(R, seen, [(s2_max, 12), (s2_ziffern, 8)])),
        ("Zahlen ordnen", mix(R, seen, [(s3_ordnen, 20)])),
        ("Zahlen dazwischen", mix(R, seen, [(s4_zwischen, 12), (s4_mitte, 8)])),
        ("Sachaufgaben zum Vergleichen", mix(R, seen, [(s5_sache, 20)])),
    ]
    body = lesson(
        ["Vergleiche zwei Zahlen <b>von vorne</b>: Zuerst die Hunderter. Sind sie gleich, dann die Zehner. Sind auch die gleich, dann die Einer.",
         "&lt; heißt <b>kleiner als</b>, &gt; heißt <b>größer als</b>. Die Spitze zeigt immer zur kleineren Zahl.",
         "Beim Ordnen schreibst du die kleinste Zahl zuerst (oder die größte, wenn es so verlangt ist)."],
        [example("Setze &lt; oder &gt; ein: 472 ☐ 427", ["Hunderter: 4 und 4, gleich", "Zehner: 7 und 2, 7 ist größer"], "472 &gt; 427"),
         example("Bilde die größte Zahl aus 5, 0 und 8.", ["größte Ziffer nach vorne: 8", "dann 5, dann 0"], "850")],
        [["Nur auf die Einer schauen: 389 &gt; 412", "Zuerst die Hunderter vergleichen: 389 &lt; 412"],
         ["Zeichen falsch herum: 300 &gt; 500", "Die Spitze zeigt zur kleineren Zahl: 300 &lt; 500"],
         ["Die 0 vorne: 058 als kleinste Zahl", "Eine dreistellige Zahl beginnt nicht mit 0: 508"]])
    faq = [
        {"q": "Wie merkt man sich die Zeichen < und >?", "a": "Die offene Seite zeigt zur größeren Zahl, die Spitze zur kleineren. Manche Kinder stellen sich ein Krokodil vor, das die größere Zahl fressen will."},
        {"q": "In welcher Reihenfolge vergleicht man?", "a": "Immer von der größten Stelle aus: Hunderter, dann Zehner, dann Einer."},
        {"q": "Was bedeutet „ordnen“?", "a": "Die Zahlen der Größe nach hinschreiben, meist von der kleinsten zur größten."},
        {"q": "Wofür braucht man das im Alltag?", "a": "Zum Beispiel beim Vergleichen von Preisen, Punkten im Spiel, Höhen oder Entfernungen."},
    ]
    make_unit(R, "zahlen-vergleichen-und-ordnen", "Z",
              "Die Schülerinnen und Schüler vergleichen und ordnen Zahlen bis 1000, nutzen die Zeichen <, > und = und begründen ihren Vergleich mit den Stellenwerten (Zusammenfassung).",
              "Zahlen vergleichen und ordnen bis 1000",
              "Zahlen vergleichen und ordnen bis 1000 – Mathe Klasse 3 Arbeitsblätter",
              "Zahlen vergleichen",
              "Mathe Klasse 3: Zahlen bis 1000 vergleichen und ordnen, größer und kleiner (<, >, =), größte Zahl aus Ziffern, Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Von vorne vergleichen: erst Hunderter, dann Zehner, dann Einer.",
              "Die Spitze von < und > zeigt zur kleineren Zahl.",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
