# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Exponentialfunktionen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k10_exponentialfunktionen.py
f(x) = a · bˣ: Funktionswerte (auch negative x), Anfangswert a und Wachstumsfaktor b, Wachstum oder Zerfall, lineares und
exponentielles Wachstum in Tabellen unterscheiden, Graphen ablesen, Eigenschaften (Asymptote, y-Achsenabschnitt), Gleichung aufstellen.
Fehler: a · bˣ = (a · b)ˣ, 2⁻³ negativ, konstante Differenzen für exponentiell gehalten, Faktor 1,05 als 5 gelesen.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, table, BLUE, RED
from de_k6 import bh, dz, endlich
from de_k10 import mcq, zahl, zr, kurve

R = random.Random(50001)


def z(v):
    v = Fr(v)
    return dz(v) if endlich(v) else bh(v)


def sup(n):
    return "<sup>%s</sup>" % (("−%d" % -n) if n < 0 else str(n))


def fx(a, b):
    a, b = Fr(a), Fr(b)
    bs = z(b)
    if b.denominator != 1 and not endlich(b):
        bs = "(%s)" % bs
    elif b.denominator != 1:
        bs = bs
    pre = "" if a == 1 else z(a) + " %s " % MAL
    return "f(x) = %s%s<sup>x</sup>" % (pre, bs)


def werte():
    a = Fr(R.choice([1, 2, 3, 4, 5, 10, 100, 50]))
    b = Fr(R.choice([2, 3, 4, 5, 10, Fr(1, 2), Fr(1, 3), Fr(1, 10)]))
    x = R.randint(-3, 4)
    v = a * b ** x
    if v.denominator > 1000 or v > 100000 or (not endlich(v) and v.denominator > 81):
        return None
    w = [z(a * b * x) if a * b * x != v and a * b * x >= 0 else z(v + 1), z((a * b) ** x) if (a * b) ** x != v and ((a * b) ** x).denominator < 10000 else z(v * 2), z(a * b ** (-x)) if x and a * b ** (-x) != v else z(v + 2)]
    if x < 0:
        w.append("−" + z(abs(a * b ** (-x))))
    return mcq("Berechne f(%s) für %s." % (dz(x), fx(a, b)), z(v), w[:3] if x >= 0 else [w[3], w[1], w[2]],
               "f(%s) = %s %s %s%s = %s %s %s = <b>%s</b>. Erst potenzieren, dann mit a multiplizieren." % (dz(x), z(a), MAL, ("(%s)" % z(b)) if b.denominator != 1 else z(b), sup(x), z(a), MAL, z(b ** x), z(v)))


def erkennen():
    a = R.choice([2, 3, 5, 10, 20, 50, 100, 200, 500])
    b = R.choice([Fr(2), Fr(3), Fr(105, 100), Fr(12, 10), Fr(15, 10), Fr(1, 2), Fr(8, 10), Fr(95, 100), Fr(9, 10), Fr(3, 4)])
    kind = R.choice(["art", "a", "b", "proz"])
    if kind == "art":
        ans = "exponentielles Wachstum" if b > 1 else "exponentielle Abnahme"
        return mcq("Beschreibt %s Wachstum oder Abnahme?" % fx(a, b), ans, ["exponentielle Abnahme" if b > 1 else "exponentielles Wachstum", "lineares Wachstum", "keine Veränderung"],
                   "b = %s ist %s 1: <b>%s</b>." % (z(b), "größer als" if b > 1 else "kleiner als", ans))
    if kind == "a":
        return mcq("Wie groß ist der Anfangswert (Wert bei x = 0) von %s?" % fx(a, b), num(a), [z(b), z(a * b), "0"],
                   "b<sup>0</sup> = 1, also f(0) = a = <b>%s</b>." % num(a))
    if kind == "b":
        return mcq("Wie groß ist der Wachstumsfaktor von %s?" % fx(a, b), z(b), [num(a), z(a * b), z(b - 1) if b > 1 else z(1 - b)],
                   "Die Basis b ist der Faktor pro Schritt: <b>%s</b>." % z(b))
    p = (b - 1) * 100
    ans = ("Zunahme um %s %% pro Schritt" % z(p)) if b > 1 else ("Abnahme um %s %% pro Schritt" % z(-p))
    return mcq("Was bedeutet der Faktor %s in %s?" % (z(b), fx(a, b)), ans,
               [("Zunahme um %s %% pro Schritt" % z(b * 100)) if b > 1 else ("Abnahme um %s %% pro Schritt" % z(b * 100)), ("Abnahme um %s %% pro Schritt" % z(abs(p))) if b > 1 else ("Zunahme um %s %% pro Schritt" % z(abs(p))), "Zunahme um %s pro Schritt" % z(b)],
               "b = 1 %s %s: <b>%s</b>." % ("+" if b > 1 else "−", z(abs(b - 1)), ans))


def tabelle():
    kind = R.choice(["exp", "lin", "faktor", "wert"])
    a = R.choice([2, 3, 4, 5, 10, 16, 64])
    if kind in ("exp", "faktor", "wert"):
        b = Fr(R.choice([2, 3, Fr(1, 2), Fr(3, 2), 4]))
        ys = [a * b ** x for x in range(4)]
        if any(y.denominator != 1 for y in ys):
            return None
    else:
        d = R.choice([3, 4, 5, 6, 8])
        ys = [a + d * x for x in range(4)]
    tab = table(["x", "0", "1", "2", "3"], [["y"] + [num(int(y)) for y in ys]])
    if kind in ("exp", "lin"):
        ans = "exponentiell (gleicher Faktor %s)" % z(b) if kind == "exp" else "linear (gleiche Differenz %d)" % d
        oth = "linear (gleiche Differenz %d)" % (ys[1] - ys[0]) if kind == "exp" else "exponentiell (gleicher Faktor %s)" % z(Fr(ys[1], ys[0]))
        return mcq(tab + "Ist das Wachstum linear oder exponentiell?", ans, [oth, "weder linear noch exponentiell", "quadratisch"],
                   ("Die Quotienten aufeinanderfolgender Werte sind gleich: <b>%s</b>." if kind == "exp" else "Die Differenzen sind gleich: <b>%s</b>.") % ans)
    if kind == "faktor":
        return mcq(tab + "Wie lautet die Funktionsgleichung?", fx(a, b), [fx(b, a) if a != b else fx(a, b + 1), "f(x) = %s + %s · x" % (num(a), num(int(ys[1] - ys[0]))), fx(a, b + 1)],
                   "Anfangswert %s, Faktor %s : %s = %s. <b>%s</b>" % (num(a), num(int(ys[1])), num(int(ys[0])), z(b), fx(a, b)))
    y4 = a * b ** 4
    if y4.denominator != 1:
        return None
    return mcq(tab + "Welcher Wert folgt für x = 4?", num(int(y4)), [num(int(ys[3] + ys[3] - ys[2])), num(int(ys[3] * b + 1)), num(int(ys[3] + b))],
               "Jeweils mal %s: %s %s %s = <b>%s</b>." % (z(b), num(int(ys[3])), MAL, z(b), num(int(y4))))


def graph():
    a = R.choice([1, 2, 3, Fr(1, 2)])
    b = R.choice([2, 3, Fr(1, 2), Fr(1, 3)])
    a, b = Fr(a), Fr(b)
    f = lambda x: float(a) * float(b) ** x
    pts = [(0, a, "")]
    x1 = 1 if b > 1 else -1
    pts.append((x1, a * b ** x1, ""))
    if a * b ** x1 > 8:
        return None
    pic = kurve([(f, BLUE, "")], (-3, 3, 1), (0, 8, 1), pts=pts, W=300, H=290, label="Graph einer Exponentialfunktion")
    kind = R.choice(["gl", "gl", "a"])
    if kind == "a":
        return mcq(pic + "Wo schneidet der Graph die y-Achse?", "bei y = %s" % z(a), ["bei y = %s" % z(b), "bei y = 0", "bei y = %s" % z(a * b) if a * b != a else "bei y = 1"],
                   "f(0) = a: <b>y = %s</b>." % z(a))
    return mcq(pic + "Welche Gleichung gehört zum Graphen?", fx(a, b), [fx(a, 1 / b), fx(b, a) if b != a else fx(a, b * 2), fx(a * 2, b) if a * 2 <= 8 else fx(a, b + 1)],
               "Der Graph schneidet die y-Achse bei %s (a). Ein Schritt nach rechts: mal %s (b). <b>%s</b>" % (z(a), z(b), fx(a, b)))


def aufstellen():
    kind = R.choice(["text", "text", "eig", "eig"])
    if kind == "text":
        a = R.choice([200, 500, 1000, 1500, 2000, 50, 80])
        p = R.choice([3, 5, 8, 10, 20, -10, -20, -5, -50])
        b = 1 + Fr(p, 100)
        if p > 0:
            t, zeit = R.choice([("Eine Bakterienkultur hat am Anfang %s Bakterien. Sie wächst pro Stunde um %d %%.", "Stunden"), ("Eine Stadt hat %s Einwohner. Die Zahl wächst pro Jahr um %d %%.", "Jahren"),
                                ("Ein Guthaben von %s € wächst pro Jahr um %d %%.", "Jahren"), ("In einem See leben %s Fische. Ihre Zahl wächst pro Jahr um %d %%.", "Jahren")])
        else:
            t, zeit = R.choice([("Ein Auto ist %s € wert. Sein Wert sinkt pro Jahr um %d %%.", "Jahren"), ("Im Blut sind %s mg eines Wirkstoffs. Die Menge sinkt pro Stunde um %d %%.", "Stunden"),
                                ("Ein Teich enthält %s Liter Wasser. Die Menge sinkt pro Woche um %d %%.", "Wochen")])
        if "Auto" in t:
            a = R.choice([8000, 12000, 20000, 25000])
        return mcq((t % (num(a), abs(p))) + " Welche Funktion beschreibt den Wert nach x %s?" % zeit, fx(a, b),
                   [fx(a, Fr(abs(p), 100)), fx(a, 1 - Fr(p, 100)), "f(x) = %s %s %s · x" % (num(a), "+" if p > 0 else "−", num(abs(p)))],
                   "Wachstumsfaktor 1 %s %s = %s: <b>%s</b>." % ("+" if p > 0 else "−", z(Fr(abs(p), 100)), z(b), fx(a, b)))
    q, a, w = R.choice([
        ("Welche Aussage gilt für jeden Graphen von f(x) = a · bˣ mit a > 0?", "Er liegt oberhalb der x-Achse.", ["Er schneidet die x-Achse.", "Er geht durch (0 | 0).", "Er ist eine Gerade."]),
        ("Welche Gerade nähert sich der Graph von f(x) = 2ˣ für x → −∞ an?", "der x-Achse (y = 0)", ["der y-Achse", "der Geraden y = 2", "der Geraden y = x"]),
        ("Durch welchen Punkt geht der Graph jeder Funktion f(x) = bˣ?", "(0 | 1)", ["(0 | 0)", "(1 | 0)", "(1 | 1)"]),
        ("Wie entsteht der Graph von g(x) = (1/2)ˣ aus dem von f(x) = 2ˣ?", "durch Spiegelung an der y-Achse", ["durch Spiegelung an der x-Achse", "durch Verschiebung nach unten", "durch Streckung um 2"]),
        ("Was gilt für f(x) = 0,8ˣ?", "Die Funktionswerte werden immer kleiner, bleiben aber positiv.", ["Die Funktionswerte werden negativ.", "Die Funktion wächst.", "Der Graph schneidet die x-Achse bei 0,8."]),
        ("Bei welchem Wachstum kommt in gleichen Zeitabständen immer derselbe Betrag dazu?", "beim linearen Wachstum", ["beim exponentiellen Wachstum", "bei beiden", "bei keinem"]),
        ("Bei welchem Wachstum wird in gleichen Zeitabständen mit demselben Faktor multipliziert?", "beim exponentiellen Wachstum", ["beim linearen Wachstum", "bei beiden", "bei keinem"]),
        ("Welcher Wachstumsfaktor gehört zu einer Zunahme um 7 %?", "1,07", ["0,07", "7", "0,93"]),
        ("Welcher Wachstumsfaktor gehört zu einer Abnahme um 15 %?", "0,85", ["0,15", "1,15", "−0,15"]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def main():
    seen = set()
    sets = [
        ("Funktionswerte", mix(R, seen, [(werte, 20)])),
        ("Anfangswert und Wachstumsfaktor", mix(R, seen, [(erkennen, 20)])),
        ("Linear oder exponentiell?", mix(R, seen, [(tabelle, 20)])),
        ("Graphen ablesen", mix(R, seen, [(graph, 20)])),
        ("Gleichungen aufstellen und Eigenschaften", mix(R, seen, [(aufstellen, 20)])),
    ]
    body = lesson(
        ["Eine <b>Exponentialfunktion</b> hat die Form f(x) = a %s b<sup>x</sup> (a ≠ 0, b &gt; 0, b ≠ 1). a ist der <b>Anfangswert</b> f(0), b der <b>Wachstumsfaktor</b>." % MAL,
         "b &gt; 1: exponentielles Wachstum. 0 &lt; b &lt; 1: exponentielle Abnahme (Zerfall). Prozent: b = 1 + p/100 bzw. b = 1 − p/100.",
         "Bei linearem Wachstum kommt pro Schritt derselbe <b>Betrag</b> dazu, bei exponentiellem Wachstum wird mit demselben <b>Faktor</b> multipliziert.",
         "Der Graph von a %s b<sup>x</sup> (a &gt; 0) liegt immer über der x-Achse und nähert sich ihr an (Asymptote)." % MAL],
        [example("f(x) = 3 %s 2<sup>x</sup>, f(4) = ?" % MAL, ["2<sup>4</sup> = 16", "3 %s 16" % MAL], "48"),
         example("Abnahme um 20 % pro Jahr", ["b = 1 − 0,2"], "b = 0,8")],
        [["3 %s 2<sup>4</sup> = 6<sup>4</sup>" % MAL, "Erst potenzieren: 3 %s 16 = 48" % MAL],
         ["2<sup>−3</sup> = −8", "2<sup>−3</sup> = 1/8"],
         ["+5 % ⇒ b = 5", "b = 1,05"]])
    faq = [
        {"q": "Was ist eine Exponentialfunktion?", "a": "Eine Funktion der Form f(x) = a · b^x. Die Variable steht im Exponenten."},
        {"q": "Woran erkenne ich exponentielles Wachstum in einer Tabelle?", "a": "Teilt man aufeinanderfolgende Werte, kommt immer derselbe Faktor heraus."},
        {"q": "Wie finde ich den Wachstumsfaktor aus einem Prozentsatz?", "a": "Bei p % Zunahme ist b = 1 + p/100, bei p % Abnahme ist b = 1 − p/100."},
        {"q": "Kann eine Exponentialfunktion null werden?", "a": "Nein. Für a > 0 sind alle Funktionswerte positiv; der Graph nähert sich der x-Achse nur an."},
    ]
    make_unit(R, "exponentialfunktionen", "F",
              "Die Schülerinnen und Schüler beschreiben exponentielle Zusammenhänge mit Funktionen f(x) = a · bˣ, deuten Anfangswert und Wachstumsfaktor, unterscheiden lineares und exponentielles Wachstum und lesen Eigenschaften aus Graphen ab (Zusammenfassung).",
              "Exponentialfunktionen",
              "Exponentialfunktionen Klasse 10 – Wachstumsfaktor, Graphen, Arbeitsblätter mit Lösungen",
              "Exponentialfunktionen",
              "Exponentialfunktionen für Klasse 10: Funktionswerte, Anfangswert und Wachstumsfaktor, linear oder exponentiell, Graphen ablesen und Gleichungen aufstellen. 100 Aufgaben mit Lösungen, kostenlos.",
              "f(x) = a · bˣ",
              "a: Anfangswert. b > 1: Wachstum, 0 < b < 1: Abnahme.",
              body, faq, sets, 1, grade="klasse-10")


if __name__ == "__main__":
    main()
