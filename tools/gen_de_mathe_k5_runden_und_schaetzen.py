# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Runden und Schätzen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_runden_und_schaetzen.py
Runden auf Zehner bis Tausender, große Zahlen runden, kleinste und größte Zahl zu einem Rundungswert, Überschlagen, sinnvoll runden.
Fehler: bei 5 abgerundet, nach der falschen Ziffer entschieden, beim Runden die restlichen Stellen nicht auf 0 gesetzt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, MAL, GETEILT, table

R = random.Random(49502)
AUF = [(10, "Zehner"), (100, "Hunderter"), (1000, "Tausender"), (10 ** 4, "Zehntausender"), (10 ** 5, "Hunderttausender"), (10 ** 6, "Millionen")]


def rd(n, s):
    return (n + s // 2) // s * s


def runden(lo, hi):
    def mk():
        s, name = R.choice(AUF[lo:hi])
        n = R.randint(s, s * 1000 if s < 10 ** 5 else s * 99)
        if n % s == 0:
            return None
        if R.random() < 0.3:
            n = n // s * s + s // 2 + (R.randint(0, s // 2 - 1) if s > 10 else 0) * 0 + (n % (s // 10) if s >= 100 else 0)
        r = rd(n, s)
        down, up = n // s * s, n // s * s + s
        w = [down if r == up else up, rd(n, s * 10) if rd(n, s * 10) != r else rd(n, s // 10 if s > 10 else s) , n // s]
        ziffer = (n // (s // 10)) % 10
        return mcq("Runde %s auf %s." % (num(n), name), num(r), [num(x) for x in dict.fromkeys(w) if x != r] + [num(r + s)],
                   "Entscheidend ist die Ziffer rechts daneben: %d. %s, also <b>%s</b>." % (ziffer, "0 bis 4 abrunden" if ziffer < 5 else "5 bis 9 aufrunden", num(r)))
    return mk


def grenzen():
    s, name = R.choice(AUF[1:4])
    r = R.randint(2, 99) * s
    kind = R.choice(["klein", "gross", "gehoert"])
    if kind == "klein":
        ans = r - s // 2
        return mcq("Eine Zahl wurde auf %s gerundet und ergab %s. Welche ist die <b>kleinste</b> natürliche Zahl, die das sein kann?" % (name, num(r)), num(ans),
                   [num(ans - 1), num(ans + 1), num(r - s)], "Ab %s wird aufgerundet: <b>%s</b>." % (num(ans), num(ans)))
    if kind == "gross":
        ans = r + s // 2 - 1
        return mcq("Eine Zahl wurde auf %s gerundet und ergab %s. Welche ist die <b>größte</b> natürliche Zahl, die das sein kann?" % (name, num(r)), num(ans),
                   [num(ans + 1), num(ans - 1) if s > 10 else num(ans - 2), num(r + s - 1)], "Ab %s würde schon auf %s aufgerundet: <b>%s</b>." % (num(ans + 1), num(r + s), num(ans)))
    good = R.randint(r - s // 2, r + s // 2 - 1)
    bads = [r - s // 2 - R.randint(1, s // 4), r + s // 2 + R.randint(0, s // 4), r + s - R.randint(1, s // 4)]
    return mcq("Welche Zahl ergibt auf %s gerundet %s?" % (name, num(r)), num(good), [num(b) for b in bads],
               "%s liegt zwischen %s und %s: <b>%s</b>." % (num(good), num(r - s // 2), num(r + s // 2 - 1), num(good)))


def ueberschlag():
    kind = R.choice(["plus", "minus", "mal", "durch"])
    if kind == "plus":
        a, b = R.randint(1100, 9800), R.randint(1100, 9800)
        e = rd(a, 1000) + rd(b, 1000)
        return mcq("Überschlage: %s + %s ≈ ?" % (num(a), num(b)), num(e), [num(e + 1000), num(e - 1000) if e > 1000 else num(e + 2000), num(e * 10)],
                   "%s + %s = <b>%s</b>. (Genau: %s)" % (num(rd(a, 1000)), num(rd(b, 1000)), num(e), num(a + b)))
    if kind == "minus":
        a, b = R.randint(5100, 9800), R.randint(1100, 4800)
        e = rd(a, 1000) - rd(b, 1000)
        return mcq("Überschlage: %s − %s ≈ ?" % (num(a), num(b)), num(e), [num(e + 1000), num(e - 1000), num(rd(a, 1000) + rd(b, 1000))],
                   "%s − %s = <b>%s</b>. (Genau: %s)" % (num(rd(a, 1000)), num(rd(b, 1000)), num(e), num(a - b)))
    if kind == "mal":
        a, b = R.randint(21, 89), R.randint(21, 89)
        e = rd(a, 10) * rd(b, 10)
        return mcq("Überschlage: %d %s %d ≈ ?" % (a, MAL, b), num(e), [num(e * 10), num(e // 10), num(rd(a, 10) + rd(b, 10))],
                   "%d %s %d = <b>%s</b>. (Genau: %s)" % (rd(a, 10), MAL, rd(b, 10), num(e), num(a * b)))
    d = R.randint(3, 9)
    q = R.randint(110, 990)
    a = q * d + R.randint(0, d - 1)
    ea = None
    for c in (rd(a, 100), rd(a, 100) + 100, rd(a, 100) - 100):
        if c % d == 0:
            ea = c
            break
    if not ea:
        return None
    e = ea // d
    return mcq("Überschlage: %s %s %d ≈ ?" % (num(a), GETEILT, d), num(e), [num(e * 10), num(e // 10), num(e + 100)],
               "Wähle eine passende Zahl in der Nähe: %s %s %d = <b>%s</b>." % (num(ea), GETEILT, d, num(e)))


SINN = [("Eine Stadt hat 248 361 Einwohner. Wie sagt man das gerundet in der Zeitung?", 248361, 1000),
        ("Ein Fußballstadion hat 81 365 Plätze. Wie viele Plätze sind das ungefähr?", 81365, 1000),
        ("Die Entfernung von Hamburg nach München beträgt 791 km. Wie weit ist das ungefähr?", 791, 100),
        ("Ein Auto kostet 23 870 €. Wie teuer ist es ungefähr?", 23870, 1000),
        ("Der Bodensee hat eine Fläche von 536 km². Wie groß ist er ungefähr?", 536, 100),
        ("Die Zugspitze ist 2962 m hoch. Wie hoch ist sie ungefähr?", 2962, 100),
        ("Ein Konzert hatte 14 728 Besucher. Wie viele waren es ungefähr?", 14728, 1000),
        ("Deutschland hat etwa 83 456 000 Einwohner. Wie viele Millionen sind das gerundet?", 83456000, 10 ** 6),
        ("Der Rhein ist 1233 km lang. Wie lang ist er ungefähr?", 1233, 100),
        ("Ein Buch hat 387 Seiten. Wie viele Seiten hat es ungefähr?", 387, 100)]


def sinn():
    order = list(range(len(SINN)))
    R.shuffle(order)
    st = {"i": 0}

    def mk():
        if st["i"] >= len(order):
            return None
        q, n, s = SINN[order[st["i"]]]
        st["i"] += 1
        r = rd(n, s)
        unit = " km" if "km" in q and "km²" not in q else " km²" if "km²" in q else " m" if "hoch" in q else " €" if "€" in q else ""
        unit = unit.replace(" ", " ")
        return mcq(q, "etwa " + num(r) + unit, ["etwa " + num(x) + unit for x in (r + s, r - s, rd(n, s * 10) if rd(n, s * 10) != r else r * 10)],
                   "Auf %s gerundet: <b>etwa %s%s</b>." % (dict(AUF)[s] if s in dict(AUF) else "Hunderter", num(r), unit))
    return mk


def main():
    seen = set()
    sets = [
        ("Runden auf Zehner, Hunderter, Tausender", mix(R, seen, [(runden(0, 3), 20)])),
        ("Große Zahlen runden", mix(R, seen, [(runden(3, 6), 20)])),
        ("Welche Zahl kann es sein?", mix(R, seen, [(grenzen, 20)])),
        ("Überschlagen", mix(R, seen, [(ueberschlag, 20)])),
        ("Sinnvoll runden", mix(R, seen, [(sinn(), 10), (grenzen, 10)])),
    ]
    body = lesson(
        ["Beim <b>Runden</b> schaust du auf die Ziffer <b>rechts neben</b> der Rundungsstelle.",
         "Bei 0, 1, 2, 3 oder 4 wird <b>abgerundet</b>, bei 5, 6, 7, 8 oder 9 wird <b>aufgerundet</b>.",
         "Alle Stellen rechts von der Rundungsstelle werden 0.",
         "Mit einem <b>Überschlag</b> prüfst du, ob ein Ergebnis ungefähr stimmen kann."],
        [example("4562 auf Hunderter", ["Ziffer rechts daneben: 6", "aufrunden"], "4600"),
         example("Überschlag 3912 + 5087", ["4000 + 5000"], "etwa 9000")],
        [["4562 auf Hunderter = 4500", "6 → aufrunden: 4600"],
         ["Bei 5 abrunden", "Bei 5 wird aufgerundet"],
         ["4562 → 4662 (nur eine Ziffer geändert)", "Rechts davon alles 0: 4600"]],
        extra=table(["Zahl", "auf Zehner", "auf Hunderter", "auf Tausender"], [["4562", "4560", "4600", "5000"], ["12 349", "12 350", "12 300", "12 000"]]))
    faq = [
        {"q": "Wann rundet man auf, wann ab?", "a": "Man schaut auf die Ziffer rechts neben der Rundungsstelle: 0 bis 4 abrunden, 5 bis 9 aufrunden."},
        {"q": "Wozu braucht man Runden?", "a": "Für Angaben in der Zeitung, für Überschläge und immer dann, wenn eine genaue Zahl nicht nötig oder nicht bekannt ist."},
        {"q": "Was ist ein Überschlag?", "a": "Eine schnelle Rechnung mit gerundeten Zahlen. Damit prüft man, ob das genaue Ergebnis ungefähr stimmt."},
        {"q": "Welche Zahlen ergeben gerundet 5000?", "a": "Auf Tausender gerundet alle Zahlen von 4500 bis 5499."},
    ]
    make_unit(R, "runden-und-schaetzen", "Z",
              "Die Schülerinnen und Schüler runden natürliche Zahlen auf verschiedene Stellen, bestimmen Zahlbereiche zu gerundeten Angaben, überschlagen Rechnungen und nutzen sinnvolle Genauigkeit in Sachsituationen (Zusammenfassung).",
              "Runden und Schätzen",
              "Runden und Überschlagen Klasse 5 – Arbeitsblätter mit Lösungen",
              "Runden",
              "Runden und Schätzen für Klasse 5: auf Zehner bis Millionen runden, kleinste und größte Zahl zu einem Rundungswert, Überschlagen und sinnvoll runden. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "0 bis 4 abrunden, 5 bis 9 aufrunden.",
              "Die Ziffer rechts neben der Rundungsstelle entscheidet.",
              body, faq, sets, 2, grade="klasse-5")


if __name__ == "__main__":
    main()
