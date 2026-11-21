# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Muster, Terme und Variablen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k5_muster_terme_und_variablen.py
Zahlenfolgen fortsetzen und Regeln finden, Figurenfolgen (Streichhölzer, Plättchen), Terme mit Variablen aufstellen und berechnen, Wertetabellen, einfache Gleichungen lösen.
Fehler: Regel nur aus den ersten zwei Zahlen geraten, 3x als 3 + x gerechnet, bei Figurenfolgen nur die neuen Teile gezählt.
"""
import random
from de_common import mcq, num, eur, lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, GREEN, FILL, INK

R = random.Random(49519)
KIDS = Kids(R)


def folge():
    kind = R.choice(["plus", "plus", "minus", "mal", "wachsend", "wechsel"])
    if kind == "plus":
        a, d = R.randint(2, 40), R.randint(3, 25)
        s = [a + i * d for i in range(5)]
        nx = a + 5 * d
        return mcq("Setze die Zahlenfolge fort: %s, …" % ", ".join(map(str, s)), str(nx), [str(nx + d), str(nx - 1), str(s[-1] + d - 1 if d > 1 else nx + 2)], "Regel: immer + %d. %d + %d = <b>%d</b>." % (d, s[-1], d, nx))
    if kind == "minus":
        d = R.randint(3, 15)
        a = R.randint(6 * d, 6 * d + 60)
        s = [a - i * d for i in range(5)]
        nx = a - 5 * d
        return mcq("Setze die Zahlenfolge fort: %s, …" % ", ".join(map(str, s)), str(nx), [str(s[-1] + d), str(nx - d), str(nx + 1)], "Regel: immer − %d. %d − %d = <b>%d</b>." % (d, s[-1], d, nx))
    if kind == "mal":
        a, f = R.randint(1, 5), R.choice([2, 3])
        s = [a * f ** i for i in range(5)]
        nx = a * f ** 5
        return mcq("Setze die Zahlenfolge fort: %s, …" % ", ".join(map(str, s)), str(nx), [str(s[-1] + (s[-1] - s[-2])), str(nx + f), str(s[-1] + f)], "Regel: immer %s %d. %d %s %d = <b>%d</b>." % (MAL, f, s[-1], MAL, f, nx))
    if kind == "wachsend":
        a, d = R.randint(1, 20), R.randint(1, 4)
        s = [a]
        for i in range(4):
            s.append(s[-1] + d + i)
        nx = s[-1] + d + 4
        return mcq("Setze die Zahlenfolge fort: %s, …" % ", ".join(map(str, s)), str(nx), [str(s[-1] + d + 3), str(s[-1] + d), str(nx + 1)],
                   "Die Abstände wachsen: +%s. Als Nächstes + %d: <b>%d</b>." % (", +".join(str(d + i) for i in range(4)), d + 4, nx))
    p, m = R.randint(3, 9), R.randint(1, 4)
    a = R.randint(10, 30)
    s = [a]
    for i in range(5):
        s.append(s[-1] + p if i % 2 == 0 else s[-1] - m)
    nx = s[-1] + p
    return mcq("Setze die Zahlenfolge fort: %s, …" % ", ".join(map(str, s)), str(nx), [str(s[-1] - m), str(nx + p), str(s[-1] + p - m)], "Regel: abwechselnd + %d und − %d. %d + %d = <b>%d</b>." % (p, m, s[-1], p, nx))


def hoelzer_svg(n):
    """Streichholzfigur: n Quadrate in einer Reihe"""
    s = []
    L = 28
    x0, y0 = 10, 12
    stick = lambda x1, y1, x2, y2: line(x1, y1, x2, y2, "#c58b3a", 4) + "<circle cx='%.1f' cy='%.1f' r='3' fill='#d23'/>" % (x2, y2)
    for i in range(n):
        x = x0 + i * L
        s.append(stick(x, y0, x + L, y0) + stick(x, y0 + L, x + L, y0 + L) + stick(x + L, y0, x + L, y0 + L))
    s.append(stick(x0, y0 + L, x0, y0))
    return wrap(x0 * 2 + n * L + 6, y0 * 2 + L + 6, "".join(s), "%d Quadrat%s aus Streichhölzern" % (n, "" if n == 1 else "e"))


def figuren():
    kind = R.choice(["quadrat", "quadrat", "plaettchen", "tisch", "turm"])
    if kind == "quadrat":
        n = R.randint(8, 30)
        pics = "".join(hoelzer_svg(k) for k in (1, 2, 3))
        return mcq(pics + "Für 1, 2 und 3 Quadrate braucht man 4, 7 und 10 Streichhölzer. Wie viele Streichhölzer braucht man für %d Quadrate?" % n, str(3 * n + 1), [str(4 * n), str(3 * n), str(3 * n + 4)],
                   "Für jedes neue Quadrat kommen 3 Hölzer dazu: 3 %s %d + 1 = <b>%d</b>." % (MAL, n, 3 * n + 1))
    if kind == "plaettchen":
        n = R.randint(6, 20)
        return mcq("Eine Figurenfolge aus Plättchen: Figur 1 hat 5, Figur 2 hat 8, Figur 3 hat 11 Plättchen. Wie viele Plättchen hat Figur %d?" % n, str(3 * n + 2), [str(5 * n), str(3 * n), str(3 * n + 5)],
                   "Es kommen immer 3 dazu: 5 + 3 %s (%d − 1) = 3 %s %d + 2 = <b>%d</b>." % (MAL, n, MAL, n, 3 * n + 2))
    if kind == "tisch":
        n = R.randint(5, 15)
        return mcq("Quadratische Tische werden in einer Reihe zusammengestellt. An einen Tisch passen 4 Personen, an 2 Tische 6, an 3 Tische 8 Personen. Wie viele Personen passen an %d Tische?" % n, str(2 * n + 2),
                   [str(4 * n), str(2 * n), str(4 * n - 2)], "Pro Tisch 2 Personen an den langen Seiten, dazu 2 an den Enden: 2 %s %d + 2 = <b>%d</b>." % (MAL, n, 2 * n + 2))
    n = R.randint(5, 12)
    t = n * (n + 1) // 2
    return mcq("Ein Treppenturm aus Würfeln: Stufe 1 hat 1 Würfel, Stufe 2 hat 1 + 2 = 3, Stufe 3 hat 1 + 2 + 3 = 6 Würfel. Wie viele Würfel hat Stufe %d?" % n, str(t), [str(n * n), str(t - n), str(2 * n)],
               "1 + 2 + … + %d = <b>%d</b>." % (n, t))


def einsetzen():
    x = R.randint(2, 12)
    kind = R.choice(["ax+b", "ax-b", "a(x+b)", "x*x", "x+x"])
    a, b = R.randint(2, 9), R.randint(1, 15)
    if kind == "ax+b":
        t, v = "%d %s x + %d" % (a, MAL, b), a * x + b
        w = [a + x + b, a * (x + b), a * 10 + x + b if x < 10 else v + a]
    elif kind == "ax-b":
        if a * x - b <= 0:
            return None
        t, v = "%d %s x − %d" % (a, MAL, b), a * x - b
        w = [a + x - b if a + x - b > 0 else v + 1, a * (x - b) if x > b else v + a, a * x + b]
    elif kind == "a(x+b)":
        t, v = "%d %s (x + %d)" % (a, MAL, b), a * (x + b)
        w = [a * x + b, a + x + b, a * x * b]
    elif kind == "x*x":
        t, v = "x %s x" % MAL, x * x
        w = [2 * x, x + x + 1, x * x + x]
    else:
        t, v = "x + x + %d" % b, 2 * x + b
        w = [x * x + b, x + b, 2 * x * b]
    return mcq("Berechne den Term %s für x = %d." % (t, x), str(v), [str(c) for c in w], "x = %d einsetzen: %s = <b>%d</b>." % (x, t.replace("x", str(x)), v))


def aufstellen():
    p, er = KIDS.next()
    kind = R.choice(["hefte", "alter", "taxi", "kino", "aelter", "teilen", "eintritt", "rest"])
    if kind == "hefte":
        pr = R.choice([2, 3, 4, 5])
        return mcq("Ein Heft kostet %d €. Welcher Term gibt den Preis für x Hefte an?" % pr, "%d %s x" % (pr, MAL), ["x + %d" % pr, "x : %d" % pr, "%d − x" % pr], "x Hefte kosten x-mal %d €: <b>%d %s x</b>." % (pr, pr, MAL))
    if kind == "alter":
        d = R.randint(2, 9)
        return mcq("%s ist x Jahre alt. Ihr Bruder ist %d Jahre älter. Welcher Term beschreibt das Alter des Bruders?" % (p if er == "sie" else "Emma", d), "x + %d" % d, ["x − %d" % d, "%d %s x" % (d, MAL), "%d − x" % d],
                   "%d Jahre älter heißt: <b>x + %d</b>." % (d, d))
    if kind == "aelter":
        f = R.choice([2, 3, 4])
        return mcq("Die Mutter ist %s so alt wie %s. %s ist x Jahre alt. Welcher Term beschreibt das Alter der Mutter?" % ({2: "doppelt", 3: "dreimal", 4: "viermal"}[f], p, p), "%d %s x" % (f, MAL), ["x + %d" % f, "x : %d" % f, "x − %d" % f],
                   "%s so alt: <b>%d %s x</b>." % ({2: "Doppelt", 3: "Dreimal", 4: "Viermal"}[f], f, MAL))
    if kind == "taxi":
        g, k = R.choice([3, 4, 5]), R.choice([2, 3])
        return mcq("Eine Taxifahrt kostet %d € Grundgebühr und %d € pro Kilometer. Welcher Term gibt den Preis für x Kilometer an?" % (g, k), "%d + %d %s x" % (g, k, MAL), ["(%d + %d) %s x" % (g, k, MAL), "%d %s x + %d %s x" % (g, MAL, k, MAL), "%d + %d + x" % (g, k)],
                   "Die Grundgebühr zahlt man einmal, die Kilometer x-mal: <b>%d + %d %s x</b>." % (g, k, MAL))
    if kind == "kino":
        pr = R.choice([6, 7, 8, 9])
        n = R.randint(3, 8)
        return mcq("Ein Kinoticket kostet x €. %s kauft %d Tickets und bezahlt %d € für Popcorn. Welcher Term beschreibt die Gesamtkosten?" % (p, n, pr), "%d %s x + %d" % (n, MAL, pr), ["%d %s (x + %d)" % (n, MAL, pr), "x + %d + %d" % (n, pr), "%d %s x %s %d" % (n, MAL, MAL, pr)],
                   "%d Tickets: %d %s x, dazu das Popcorn: <b>%d %s x + %d</b>." % (n, n, MAL, n, MAL, pr))
    if kind == "teilen":
        n = R.choice([3, 4, 5, 6])
        return mcq("x Bonbons werden gerecht an %d Kinder verteilt. Welcher Term gibt an, wie viele jedes Kind bekommt?" % n, "x : %d" % n, ["%d : x" % n, "%d %s x" % (n, MAL), "x − %d" % n], "Gerecht verteilen heißt teilen: <b>x : %d</b>." % n)
    if kind == "eintritt":
        e, k = R.choice([(9, 5), (12, 6), (10, 4)])
        return mcq("Der Eintritt kostet %d € für Erwachsene und %d € für Kinder. Welcher Term gibt den Preis für a Erwachsene und k Kinder an?" % (e, k), "%d %s a + %d %s k" % (e, MAL, k, MAL), ["(%d + %d) %s (a + k)" % (e, k, MAL), "%d + a + %d + k" % (e, k), "%d %s k + %d %s a" % (e, MAL, k, MAL)],
                   "Erwachsene: %d %s a, Kinder: %d %s k. <b>%d %s a + %d %s k</b>." % (e, MAL, k, MAL, e, MAL, k, MAL))
    g = R.choice([20, 50, 100])
    return mcq("%s hat %d € und kauft x Bücher zu je 8 €. Welcher Term gibt an, wie viel Geld übrig bleibt?" % (p, g), "%d − 8 %s x" % (g, MAL), ["8 %s x − %d" % (MAL, g), "(%d − 8) %s x" % (g, MAL), "%d − x − 8" % g],
               "Ausgaben: 8 %s x. Vom Geld abziehen: <b>%d − 8 %s x</b>." % (MAL, g, MAL))


def tabelle():
    a, b = R.randint(2, 7), R.randint(0, 9)
    xs = sorted(R.sample(range(1, 11), 4))
    ys = [a * x + b for x in xs]
    kind = R.choice(["fehlt", "regel"])
    if kind == "fehlt":
        k = R.randint(1, 3)
        shown = ["?" if i == k else str(y) for i, y in enumerate(ys)]
        tab = table(["x"] + [str(x) for x in xs], [["y"] + shown])
        return mcq(tab + "Die Tabelle gehört zur Regel y = %d %s x + %d. Welche Zahl gehört an die Stelle des Fragezeichens?" % (a, MAL, b), str(ys[k]), [str(ys[k] + a), str(a * xs[k]), str(ys[k] - 1)],
                   "%d %s %d + %d = <b>%d</b>." % (a, MAL, xs[k], b, ys[k]))
    tab = table(["x"] + [str(x) for x in xs], [["y"] + [str(y) for y in ys]])
    ans = "y = %d %s x + %d" % (a, MAL, b) if b else "y = %d %s x" % (a, MAL)
    w = ["y = x + %d" % (ys[0] - xs[0]), "y = %d %s x + %d" % (a + 1, MAL, b - xs[0]) if b - xs[0] > 0 else "y = %d %s x" % (a + 1, MAL), "y = %d %s x + %d" % (a, MAL, b + 1)]
    return mcq(tab + "Welche Regel passt zu allen Paaren der Tabelle?", ans, w, "Prüfe jedes Paar, z. B. x = %d: %d %s %d + %d = %d. <b>%s</b>." % (xs[-1], a, MAL, xs[-1], b, ys[-1], ans))


def gleichung():
    kind = R.choice(["plus", "minus", "mal", "zwei", "zwei"])
    x = R.randint(2, 15)
    if kind == "plus":
        b = R.randint(3, 40)
        return mcq("Löse: x + %d = %d" % (b, x + b), "x = %d" % x, ["x = %d" % (x + 2 * b), "x = %d" % (x + 1), "x = %d" % b], "Umkehraufgabe: %d − %d = <b>%d</b>. Probe: %d + %d = %d." % (x + b, b, x, x, b, x + b))
    if kind == "minus":
        b = R.randint(3, 30)
        return mcq("Löse: x − %d = %d" % (b, x), "x = %d" % (x + b), ["x = %d" % abs(x - b) if x != b else "x = %d" % (x + b + 1), "x = %d" % x, "x = %d" % (x + b + 1)], "Umkehraufgabe: %d + %d = <b>%d</b>." % (x, b, x + b))
    if kind == "mal":
        a = R.randint(2, 9)
        return mcq("Löse: %d %s x = %d" % (a, MAL, a * x), "x = %d" % x, ["x = %d" % (a * x - a), "x = %d" % (a * x * a), "x = %d" % (x + 1)], "Umkehraufgabe: %d : %d = <b>%d</b>." % (a * x, a, x))
    a, b = R.randint(2, 8), R.randint(1, 20)
    r = a * x + b
    return mcq("Löse: %d %s x + %d = %d" % (a, MAL, b, r), "x = %d" % x, ["x = %d" % ((r + b) // a) if (r + b) % a == 0 and (r + b) // a != x else "x = %d" % (x + 2), "x = %d" % (r - b), "x = %d" % (x - 1)],
               "Erst − %d: %d %s x = %d. Dann : %d: <b>x = %d</b>. Probe: %d %s %d + %d = %d." % (b, a, MAL, r - b, a, x, a, MAL, x, b, r))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["taxi", "handy", "sparen", "kerzen", "zahl", "zahl2"])
    if kind == "taxi":
        g, k = R.choice([3, 4, 5]), R.choice([2, 3])
        x = R.randint(4, 15)
        return mcq("Ein Taxi kostet %d € Grundgebühr und %d € pro Kilometer. Was kostet eine Fahrt über %d km?" % (g, k, x), "%d €" % (g + k * x), ["%d €" % c for c in ((g + k) * x, g + k + x, k * x)],
                   "%d + %d %s %d = <b>%d €</b>." % (g, k, MAL, x, g + k * x))
    if kind == "handy":
        g, k = R.choice([5, 8, 10]), R.choice([2, 3])
        t = g + k * R.randint(3, 10)
        x = (t - g) // k
        return mcq("Ein Handytarif kostet %d € im Monat plus %d € pro GB Daten. %s bezahlt %d €. Wie viele GB hat %s verbraucht?" % (g, k, p, t, er), str(x), [str(t // k), str(t - g), str(x + 1)],
                   "%d − %d = %d. %d : %d = <b>%d</b> GB." % (t, g, t - g, t - g, k, x))
    if kind == "sparen":
        s, w = R.randint(10, 60), R.choice([4, 5, 6, 8])
        n = R.randint(4, 12)
        return mcq("%s hat %d € und spart jede Woche %d €. Wie viel Geld hat %s nach %d Wochen? (Term: %d + %d %s x)" % (p, s, w, er, n, s, w, MAL), "%d €" % (s + w * n), ["%d €" % c for c in ((s + w) * n, s + w + n, w * n)],
                   "x = %d: %d + %d %s %d = <b>%d €</b>." % (n, s, w, MAL, n, s + w * n))
    if kind == "kerzen":
        h, d = R.choice([20, 24, 30]), R.choice([2, 3])
        x = R.randint(2, h // d - 1)
        return mcq("Eine Kerze ist %d cm hoch und brennt jede Stunde %d cm ab. Wie hoch ist sie nach %d Stunden? (Term: %d − %d %s x)" % (h, d, x, h, d, MAL), "%d cm" % (h - d * x), ["%d cm" % c for c in (h - x, d * x, h - d - x)],
                   "%d − %d %s %d = <b>%d cm</b>." % (h, d, MAL, x, h - d * x))
    if kind == "zahl":
        a, b = R.randint(2, 6), R.randint(3, 20)
        x = R.randint(3, 15)
        return mcq("Ich denke mir eine Zahl. Ich multipliziere sie mit %d und addiere %d. Ich erhalte %d. Wie heißt die Zahl?" % (a, b, a * x + b), str(x), [str(a * x), str((a * x + b) // a), str(x + 1)],
                   "Rückwärts: %d − %d = %d, %d : %d = <b>%d</b>." % (a * x + b, b, a * x, a * x, a, x)) if (a * x + b) // a != x else None
    a = R.randint(3, 20)
    x = R.randint(5, 40)
    return mcq("Ich denke mir eine Zahl und addiere %d. Das Ergebnis verdopple ich und erhalte %d. Wie heißt die Zahl?" % (a, 2 * (x + a)), str(x), [str(2 * (x + a) - a), str(x + a), str((2 * (x + a) - a) // 2)],
               "Rückwärts: %d : 2 = %d, %d − %d = <b>%d</b>." % (2 * (x + a), x + a, x + a, a, x))


def main():
    seen = set()
    sets = [
        ("Zahlenfolgen fortsetzen", mix(R, seen, [(folge, 20)])),
        ("Figurenfolgen", mix(R, seen, [(figuren, 14), (folge, 6)])),
        ("Terme mit Variablen", mix(R, seen, [(einsetzen, 10), (aufstellen, 10)])),
        ("Tabellen und Gleichungen", mix(R, seen, [(tabelle, 8), (gleichung, 12)])),
        ("Sachaufgaben mit Termen", mix(R, seen, [(sache, 14), (aufstellen, 6)])),
    ]
    body = lesson(
        ["Bei einer <b>Zahlenfolge</b> suchst du die Regel. Prüfe sie an <b>allen</b> Zahlen, nicht nur an den ersten beiden.",
         "Eine <b>Variable</b> (z. B. x) ist ein Platzhalter für eine Zahl. 3 %s x heißt: 3 mal die Zahl x." % MAL,
         "Einen Term berechnet man, indem man für die Variable eine Zahl einsetzt. Es gilt Punkt vor Strich.",
         "Eine einfache <b>Gleichung</b> löst du mit der Umkehraufgabe. Mache dann die Probe."],
        [example("4 %s x + 3 für x = 5" % MAL, ["4 %s 5 = 20" % MAL, "20 + 3"], "23"),
         example("3 %s x + 4 = 19" % MAL, ["19 − 4 = 15", "15 : 3 = 5", "Probe: 3 %s 5 + 4 = 19" % MAL], "x = 5")],
        [["3 %s x für x = 4: 3 + 4 = 7" % MAL, "3 %s 4 = 12" % MAL],
         ["Regel aus 2, 4 geraten: + 2", "Bei 2, 4, 8, 16 ist die Regel %s 2" % MAL],
         ["3 Hölzer pro Quadrat: 5 Quadrate = 15", "Das erste Holz links zählt extra: 3 %s 5 + 1 = 16" % MAL]])
    faq = [
        {"q": "Was ist eine Variable?", "a": "Ein Buchstabe, der für eine Zahl steht. Man kann verschiedene Zahlen einsetzen."},
        {"q": "Wie finde ich die Regel einer Zahlenfolge?", "a": "Schau dir die Unterschiede zwischen den Zahlen an. Sind sie immer gleich, wird immer dasselbe addiert. Sonst prüfe, ob multipliziert wird oder die Abstände wachsen."},
        {"q": "Wie löse ich eine Gleichung wie 4 · x + 2 = 30?", "a": "Rechne rückwärts: 30 − 2 = 28, dann 28 : 4 = 7. Probe: 4 · 7 + 2 = 30."},
        {"q": "Was bedeutet 3 · x + 2?", "a": "Man nimmt die Zahl x dreimal und addiert dann 2."},
    ]
    make_unit(R, "muster-terme-und-variablen", "F",
              "Die Schülerinnen und Schüler setzen Zahlen- und Figurenfolgen fort, beschreiben Regeln, stellen Terme mit Variablen auf, berechnen Termwerte und lösen einfache Gleichungen (Zusammenfassung).",
              "Muster, Terme und Variablen",
              "Muster, Terme und Variablen Klasse 5 – Arbeitsblätter mit Lösungen",
              "Terme & Variablen",
              "Muster und Terme für Klasse 5: Zahlenfolgen, Figurenfolgen, Terme mit Variablen, Tabellen und einfache Gleichungen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Eine Variable ist ein Platzhalter für eine Zahl.",
              "Gleichungen löst du mit der Umkehraufgabe – dann die Probe.",
              body, faq, sets, 19, grade="klasse-5")


if __name__ == "__main__":
    main()
