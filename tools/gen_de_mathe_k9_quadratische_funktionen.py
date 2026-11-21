# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Quadratische Funktionen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k9_quadratische_funktionen.py
Normalparabel, Funktionswerte, Streckung und Öffnung (y = ax²), Verschiebung (y = (x − d)² + e), Scheitelpunkt ablesen,
Graphen zuordnen, Sachaufgaben (Wurf, Brückenbogen, Flächen).
Fehler: (x − 3)² verschiebt nach links, (−3)² = −9, a = 0,5 für „gestreckt“ gehalten, Scheitel (d | e) mit falschem Vorzeichen.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, table, BLUE, RED
from de_k9 import mcq, zahl, sform, qf, parabel, par

R = random.Random(49903)


def zd(v):
    from de_k6 import dz, endlich
    v = Fr(v)
    return dz(v) if endlich(v) else zahl(v)


def S(d, e):
    return "S(%s | %s)" % (zahl(d), zahl(e))


def werte():
    a = R.choice([1, 1, 2, 3, -1, -2, Fr(1, 2), Fr(-1, 2)])
    d, e = R.randint(-3, 3), R.randint(-5, 5)
    kind = R.choice(["wert", "wert", "tab", "neg"])
    if kind == "neg":
        x = R.randint(-6, -2)
        return mcq("Berechne f(%s) für f(x) = x²." % zahl(x), zahl(x * x), [zahl(-x * x), zahl(2 * x), zahl(-2 * x)],
                   "(%s)² = (%s) %s (%s) = <b>%s</b>. Minus mal Minus ergibt Plus." % (zahl(x), zahl(x), MAL, zahl(x), zahl(x * x)))
    f = lambda x: a * (x - d) ** 2 + e
    if kind == "wert":
        x = R.randint(-4, 5)
        y = f(x)
        if y.denominator != 1:
            return None
        return mcq("Berechne f(%s) für f(x) = %s." % (zahl(x), sform(a, d, e).split("= ", 1)[1]), zahl(y), [zahl(a * (x - d) * 2 + e), zahl(a * (x + d) ** 2 + e) if d else zahl(y + 1), zahl(a * x * x - d * d + e) if d else zahl(-y) if y else "1"],
                   "Erst die Klammer: %s − %s = %s, quadrieren: %s, dann weiter: <b>%s</b>." % (zahl(x), par(d), zahl(x - d), zahl((x - d) ** 2), zahl(y)))
    xs = [-2, -1, 0, 1, 2]
    a2 = R.choice([1, 2, -1, 3])
    c = R.randint(-4, 4)
    ys = [a2 * x * x + c for x in xs]
    miss = R.choice([0, 1, 3, 4])
    tab = table(["x"] + [zahl(x) for x in xs], [["y"] + [zahl(y) if i != miss else "?" for i, y in enumerate(ys)]])
    return mcq(tab + "Die Tabelle gehört zu %s. Welche Zahl fehlt?" % sform(a2, 0, c), zahl(ys[miss]), [zahl(-a2 * xs[miss] ** 2 + c), zahl(a2 * 2 * xs[miss] + c), zahl(ys[miss] + a2)],
               "x = %s: %s %s %s² %s = <b>%s</b>." % (zahl(xs[miss]), zahl(a2), MAL, par(xs[miss]), ("+ %s" % zahl(c)) if c >= 0 else ("− %s" % zahl(-c)), zahl(ys[miss])))


def streckung():
    kind = R.choice(["offen", "form", "form", "breit"])
    a = Fr(R.choice([2, 3, 4, -2, -3, -1, Fr(1, 2), Fr(1, 3), Fr(-1, 2), Fr(-1, 4), Fr(3, 2), Fr(5, 2)]))
    if kind == "offen":
        ans = "nach oben" if a > 0 else "nach unten"
        return mcq("Ist die Parabel %s nach oben oder nach unten geöffnet?" % sform(a, 0, R.randint(-4, 4)), ans, ["nach unten" if a > 0 else "nach oben", "nach rechts", "Das hängt vom Scheitelpunkt ab."],
                   "a = %s ist %s: <b>%s</b>." % (zahl(a), "positiv" if a > 0 else "negativ", ans))
    if kind == "form":
        if abs(a) == 1:
            return None
        ans = "gestreckt (enger als die Normalparabel)" if abs(a) > 1 else "gestaucht (weiter als die Normalparabel)"
        oth = "gestaucht (weiter als die Normalparabel)" if abs(a) > 1 else "gestreckt (enger als die Normalparabel)"
        return mcq("Wie verändert der Faktor in %s die Form im Vergleich zur Normalparabel?" % sform(a, 0, 0), ans, [oth, "nur verschoben, Form gleich", "an der x-Achse gespiegelt, Form gleich"],
                   "|a| = %s ist %s 1: <b>%s</b>.%s" % (zahl(abs(a)), "größer als" if abs(a) > 1 else "kleiner als", ans.split(" (")[0], " Das Minus spiegelt zusätzlich an der x-Achse." if a < 0 else ""))
    l = [Fr(3), Fr(1, 2), Fr(-2), Fr(1)]
    R.shuffle(l)
    best = max(l, key=lambda v: (abs(v), v))
    return mcq("Welche Parabel ist am engsten?", sform(best, 0, 0), [sform(v, 0, 0) for v in l if v != best],
               "Am engsten ist die Parabel mit dem größten |a|: <b>%s</b>." % sform(best, 0, 0))


def scheitel():
    a = R.choice([1, 1, 2, -1, -2, Fr(1, 2), 3])
    d, e = R.randint(-6, 6), R.randint(-6, 6)
    if d == 0 and e == 0:
        return None
    kind = R.choice(["s", "s", "verschieb", "gl"])
    if kind == "s":
        return mcq("Gib den Scheitelpunkt von %s an." % sform(a, d, e), S(d, e), [S(-d, e) if d else S(d, -e), S(e, d) if d != e else S(d + 1, e), S(-d, -e) if (d or e) else S(1, 1)],
                   "y = a(x − d)² + e hat den Scheitel S(d | e). Achtung: (x %s %s) bedeutet d = %s. <b>%s</b>" % ("−" if d >= 0 else "+", zahl(abs(d)), zahl(d), S(d, e)))
    if kind == "verschieb":
        if d == 0 or e == 0:
            return None
        ans = "um %s nach %s und um %s nach %s" % (zahl(abs(d)), "rechts" if d > 0 else "links", zahl(abs(e)), "oben" if e > 0 else "unten")
        wr = ["um %s nach %s und um %s nach %s" % (zahl(abs(d)), "links" if d > 0 else "rechts", zahl(abs(e)), "oben" if e > 0 else "unten"),
              "um %s nach %s und um %s nach %s" % (zahl(abs(e)), "rechts" if e > 0 else "links", zahl(abs(d)), "oben" if d > 0 else "unten"),
              "um %s nach %s und um %s nach %s" % (zahl(abs(d)), "rechts" if d > 0 else "links", zahl(abs(e)), "unten" if e > 0 else "oben")]
        return mcq("Wie entsteht der Graph von %s aus der Normalparabel?" % sform(1, d, e), ans, wr,
                   "Scheitel %s: <b>%s</b>." % (S(d, e), ans))
    return mcq("Eine Normalparabel wird so verschoben, dass ihr Scheitel bei %s liegt. Wie lautet die Gleichung?" % S(d, e), sform(1, d, e),
               [sform(1, -d, e) if d else sform(1, d, -e), sform(1, e, d) if d != e else sform(1, d, e + 1), sform(1, -d, -e) if d and e else sform(2, d, e)],
               "y = (x − d)² + e mit d = %s, e = %s: <b>%s</b>." % (zahl(d), zahl(e), sform(1, d, e)))


def graph():
    a = Fr(R.choice([1, 1, -1, 2, Fr(1, 2), -2, Fr(-1, 2)]))
    d, e = R.randint(-3, 3), R.randint(-3, 3)
    pic = parabel([(a, d, e, BLUE, "")], pts=[(d, e, "S")], label="Graph einer quadratischen Funktion")
    kind = R.choice(["s", "gl", "gl"])
    if kind == "s":
        return mcq(pic + "Lies den Scheitelpunkt ab.", S(d, e), [S(e, d) if d != e else S(d + 1, e), S(-d, e) if d else S(d, -e) if e else S(1, 0), S(d, -e) if e else S(-1, e)],
                   "Der tiefste bzw. höchste Punkt: <b>%s</b>." % S(d, e))
    return mcq(pic + "Welche Gleichung gehört zum Graphen?", sform(a, d, e), [sform(a, -d, e) if d else sform(a, d, -e) if e else sform(a, 1, 0), sform(-a, d, e), sform(a * 2 if abs(a) < 2 else a / 4, d, e)],
               "Scheitel %s, %s geöffnet, %s: <b>%s</b>." % (S(d, e), "nach oben" if a > 0 else "nach unten", "Normalparabel-Form" if abs(a) == 1 else ("gestreckt" if abs(a) > 1 else "gestaucht"), sform(a, d, e)))


def sache():
    kind = R.choice(["wurf", "wurf", "bruecke", "flaeche", "brems"])
    if kind == "wurf":
        d, e = R.choice([(2, 5), (3, 6), (4, 8), (5, 10), (3, 9), (2, 4)])
        a = Fr(-R.choice([1, 2]), R.choice([2, 4, 5]))
        ask = R.choice(["hoehe", "weite"])
        if ask == "hoehe":
            return mcq("Ein Ball fliegt auf der Bahn %s (x und y in m). Wie hoch fliegt er höchstens?" % sform(a, d, e), "%s m" % zd(e), ["%s m" % zd(d), "%s m" % zd(e - a), "%s m" % zd(2 * d)],
                       "Der Scheitel S(%s | %s) ist der höchste Punkt: <b>%s m</b>." % (zd(d), zd(e), zd(e)))
        return mcq("Ein Ball fliegt auf der Bahn %s (x und y in m). In welcher waagrechten Entfernung erreicht er seine größte Höhe?" % sform(a, d, e), "nach %s m" % zd(d), ["nach %s m" % zd(e), "nach %s m" % zd(-d), "nach %s m" % zd(2 * d)],
                   "Der Scheitel liegt bei x = d = <b>%s m</b>." % zd(d))
    if kind == "bruecke":
        h, w = R.choice([(8, 20), (10, 40), (6, 24), (12, 30), (9, 30)])
        a = Fr(-h * 4, w * w)
        x = R.choice([w // 4, w // 5])
        y = a * x * x + h
        if y.denominator != 1 and (y * 10).denominator != 1:
            return None
        return mcq("Ein Brückenbogen hat die Form y = %s (Scheitel in der Mitte, x und y in m). Wie hoch ist der Bogen %s m neben der Mitte?" % (qf(a, 0, h).replace("x²", "x²"), zd(x)), "%s m" % zd(y),
                   ["%s m" % zd(h), "%s m" % zd(h - a * x * x), "%s m" % zd(h + a * x)],
                   "y = %s %s %s² + %d = <b>%s m</b>." % (zd(a), MAL, zd(x), h, zd(y)))
    if kind == "flaeche":
        x = R.randint(2, 12)
        k = R.randint(2, 5)
        return mcq("Ein Quadrat mit der Seite x cm wird an einer Seite um %d cm verlängert. Der Flächeninhalt ist A(x) = x² + %dx. Wie groß ist A für x = %d?" % (k, k, x), "%d cm²" % (x * x + k * x), ["%d cm²" % ((x + k) ** 2), "%d cm²" % (x * x + k), "%d cm²" % (2 * x + k * x)],
                   "%d² + %d %s %d = %d + %d = <b>%d cm²</b>." % (x, k, MAL, x, x * x, k * x, x * x + k * x))
    v = R.choice([30, 50, 60, 80, 100])
    return mcq("Für den Bremsweg gilt ungefähr s = (v : 10)² (s in m, v in km/h). Wie lang ist der Bremsweg bei %d km/h?" % v, "%d m" % ((v // 10) ** 2), ["%d m" % (v // 10 * 2), "%d m" % (v * v // 10), "%d m" % (v // 10)],
               "(%d : 10)² = %d² = <b>%d m</b>. Doppelte Geschwindigkeit bedeutet vierfachen Bremsweg." % (v, v // 10, (v // 10) ** 2))


def main():
    seen = set()
    sets = [
        ("Funktionswerte", mix(R, seen, [(werte, 20)])),
        ("Öffnung und Streckung", mix(R, seen, [(streckung, 20)])),
        ("Scheitelpunkt und Verschiebung", mix(R, seen, [(scheitel, 20)])),
        ("Graphen ablesen", mix(R, seen, [(graph, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Der Graph von y = x² heißt <b>Normalparabel</b>. Ihr tiefster Punkt ist der <b>Scheitelpunkt</b> S(0 | 0).",
         "y = a %s x²: a &gt; 0 nach oben geöffnet, a &lt; 0 nach unten. |a| &gt; 1 gestreckt (enger), |a| &lt; 1 gestaucht (weiter)." % MAL,
         "<b>Scheitelpunktform</b> y = a(x − d)² + e: Scheitel S(d | e). Die Parabel ist um d nach rechts und um e nach oben verschoben.",
         "Achtung: In (x + 2)² ist d = −2, die Parabel ist nach <b>links</b> verschoben."],
        [example("y = (x − 3)² + 1", ["d = 3, e = 1"], "S(3 | 1)"),
         example("y = −2(x + 1)² + 4", ["a = −2: nach unten, gestreckt", "d = −1, e = 4"], "S(−1 | 4)")],
        [["(x − 3)²: 3 nach links", "x − 3: 3 nach rechts"],
         ["(−3)² = −9", "(−3)² = 9"],
         ["y = 0,5x² ist gestreckt", "|a| &lt; 1: gestaucht"]])
    faq = [
        {"q": "Was ist der Scheitelpunkt?", "a": "Der tiefste Punkt einer nach oben geöffneten Parabel bzw. der höchste Punkt einer nach unten geöffneten Parabel."},
        {"q": "Wie lese ich den Scheitelpunkt aus y = a(x − d)² + e ab?", "a": "S(d | e). Bei (x + 4)² ist d = −4."},
        {"q": "Was bewirkt der Faktor a?", "a": "Das Vorzeichen bestimmt die Öffnung, der Betrag die Form: |a| > 1 enger, |a| < 1 weiter als die Normalparabel."},
        {"q": "Wo begegnen mir Parabeln?", "a": "Bei Wurfbahnen, Brückenbögen, Bremswegen und bei Flächen, die von x² abhängen."},
    ]
    make_unit(R, "quadratische-funktionen", "F",
              "Die Schülerinnen und Schüler beschreiben quadratische Funktionen mit Term, Tabelle und Graph, deuten Streckung, Öffnung und Verschiebung, bestimmen Scheitelpunkte und nutzen quadratische Funktionen in Sachsituationen (Zusammenfassung).",
              "Quadratische Funktionen",
              "Quadratische Funktionen Klasse 9 – Parabel, Scheitelpunkt, Arbeitsblätter mit Lösungen",
              "Parabeln",
              "Quadratische Funktionen für Klasse 9: Normalparabel, Funktionswerte, Streckung und Öffnung, Scheitelpunktform, Graphen ablesen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "y = a(x − d)² + e hat den Scheitel S(d | e).",
              "a > 0: nach oben geöffnet. |a| > 1: gestreckt.",
              body, faq, sets, 3, grade="klasse-9")


if __name__ == "__main__":
    main()
