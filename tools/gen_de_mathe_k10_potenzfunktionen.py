# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Potenzfunktionen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k10_potenzfunktionen.py
f(x) = a · xⁿ (n ganzzahlig, auch negativ), gerade und ungerade Exponenten, Symmetrie, gemeinsame Punkte, Definitions- und Wertebereich,
Hyperbeln mit Asymptoten, Wurzelfunktionen x^(1/2), x^(1/3), Graphen zuordnen, Gleichungen xⁿ = c, Anwendungen (Fläche, Volumen, Fallweg).
Fehler: (−2)⁴ negativ, 2⁻² = −4, x⁴ = 81 nur x = 3, Verdoppeln der Kante verdoppelt das Volumen.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, BLUE
from de_k6 import bh, dz, endlich
from de_k10 import mcq, zr, kurve

R = random.Random(50004)
M = "−"


def z(v):
    v = Fr(v)
    if v < 0:
        return M + z(-v)
    return dz(v) if endlich(v) and v.denominator <= 8 else bh(v)


def sup(n):
    return "<sup>%s</sup>" % ((M + str(-n)) if n < 0 else str(n))


def fx(a, n, name="f"):
    a = Fr(a)
    pre = "" if a == 1 else (M if a == -1 else z(a) + " %s " % MAL)
    return "%s(x) = %sx%s" % (name, pre, sup(n) if n != 1 else "")


def par(v):
    return "(%s)" % z(v) if Fr(v) < 0 else z(v)


def werte():
    a = Fr(R.choice([1, 1, 2, 3, -1, -2, Fr(1, 2)]))
    n = R.choice([2, 3, 4, 5, -1, -2, -3])
    x = Fr(R.choice([-3, -2, -1, 2, 3, Fr(1, 2), -Fr(1, 2), 4]))
    if abs(n) > 3 and abs(x) > 2:
        return None
    v = a * x ** n
    if abs(v) > 1000 or v.denominator > 100:
        return None
    w = [z(-v), z(a * x * n), z(a * (-abs(x)) ** n * -1) if a * x * n == -v else z(a * Fr(1, x) ** n)]
    if n < 0:
        w = [z(a * x * n), z(-a * abs(x) ** (-n)) if -a * abs(x) ** (-n) != v else z(-v), z(a * x ** (-n))]
    return mcq("Berechne f(%s) für %s." % (z(x), fx(a, n)), z(v), w,
               "f(%s) = %s%s%s = <b>%s</b>." % (z(x), (z(a) + " " + MAL + " ") if a != 1 else "", par(x) if x.denominator == 1 else "(%s)" % z(x), sup(n), z(v))
               + (" Negativer Exponent: x%s = 1 : x%s." % (sup(n), sup(-n) if n != -1 else "") if n < 0 else (" Gerader Exponent: %s%s ist positiv." % (par(x), sup(n)) if n % 2 == 0 and x < 0 else "")))


def eigenschaften():
    n = R.choice([2, 3, 4, 5, 6, 7, -1, -2, -3, -4])
    kind = R.choice(["sym", "punkt", "wb", "db", "verlauf"])
    g = n % 2 == 0
    if kind == "sym":
        ans = "achsensymmetrisch zur y-Achse" if g else "punktsymmetrisch zum Ursprung"
        return mcq("Welche Symmetrie hat der Graph von %s?" % fx(1, n), ans,
                   ["punktsymmetrisch zum Ursprung" if g else "achsensymmetrisch zur y-Achse", "achsensymmetrisch zur x-Achse", "keine Symmetrie"],
                   "Der Exponent %s ist %s: <b>%s</b>." % (z(n), "gerade" if g else "ungerade", ans))
    if kind == "punkt":
        ans = "(−1 | 1)" if g else "(−1 | −1)"
        return mcq("Durch welchen Punkt verläuft der Graph von %s außer (1 | 1)?" % fx(1, n), ans,
                   ["(−1 | −1)" if g else "(−1 | 1)", "(0 | 1)", "(1 | 0)"] if n < 0 else ["(−1 | −1)" if g else "(−1 | 1)", "(0 | 1)", "(2 | %s)" % z(2 * n)],
                   "(−1)%s = %s, also <b>%s</b>." % (sup(n), "1" if g else M + "1", ans))
    if kind == "wb":
        if n > 0:
            ans = "W = ℝ₀⁺ (alle y ≥ 0)" if g else "W = ℝ (alle reellen Zahlen)"
            wr = ["W = ℝ (alle reellen Zahlen)" if g else "W = ℝ₀⁺ (alle y ≥ 0)", "W = ℝ⁺ (alle y &gt; 0)", "W = ℝ ∖ {0}"]
        else:
            ans = "W = ℝ⁺ (alle y &gt; 0)" if g else "W = ℝ ∖ {0}"
            wr = ["W = ℝ ∖ {0}" if g else "W = ℝ⁺ (alle y &gt; 0)", "W = ℝ₀⁺ (alle y ≥ 0)", "W = ℝ (alle reellen Zahlen)"]
        return mcq("Welchen Wertebereich hat %s?" % fx(1, n), ans, wr, "%s<b>%s</b>." % ("Gerader Exponent: keine negativen Werte. " if g else "", ans))
    if kind == "db":
        if n > 0:
            return None
        return mcq("Welche Definitionsmenge hat %s?" % fx(1, n), "D = ℝ ∖ {0}", ["D = ℝ", "D = ℝ⁺", "D = ℝ ∖ {1}"],
                   "x%s = 1 : x%s. Durch 0 darf man nicht teilen: <b>D = ℝ ∖ {0}</b>." % (sup(n), sup(-n) if n != -1 else ""))
    if n > 0:
        if g:
            ans = "fällt für x &lt; 0 und steigt für x &gt; 0"
            wr = ["steigt überall", "fällt überall", "steigt für x &lt; 0 und fällt für x &gt; 0"]
        else:
            ans = "steigt überall"
            wr = ["fällt für x &lt; 0 und steigt für x &gt; 0", "fällt überall", "steigt für x &lt; 0 und fällt für x &gt; 0"]
    else:
        if g:
            ans = "steigt für x &lt; 0 und fällt für x &gt; 0"
            wr = ["fällt für x &lt; 0 und steigt für x &gt; 0", "steigt überall", "fällt überall"]
        else:
            ans = "fällt für x &lt; 0 und fällt für x &gt; 0"
            wr = ["steigt für x &lt; 0 und steigt für x &gt; 0", "fällt für x &lt; 0 und steigt für x &gt; 0", "steigt überall"]
    return mcq("Wie verläuft der Graph von %s?" % fx(1, n), "Er " + ans + ".", ["Er " + t + "." for t in wr],
               "Setze Werte ein, z. B. x = −2, −1, 1, 2: <b>Er %s.</b>" % ans)


def graph():
    a = Fr(R.choice([1, 1, -1, 2, Fr(1, 2)]))
    n = R.choice([2, 3, 4, -1, -2])
    f = lambda x: float(a) * x ** n
    pic = kurve([(f, BLUE, "")], (-3, 3, 1), (-4, 4, 1), W=300, H=300, label="Graph einer Potenzfunktion")
    others = [(a, m) for m in [2, 3, 4, -1, -2] if m != n] + [(-a, n)]
    w = [fx(b, m) for b, m in R.sample(others, 3)]
    return mcq(pic + "Welche Funktionsgleichung gehört zum Graphen?", fx(a, n), w,
               "%s, %s. Der Punkt (1 | %s) liegt auf dem Graphen: <b>%s</b>." % (
                   "Symmetrisch zur y-Achse" if n % 2 == 0 else "Punktsymmetrisch zum Ursprung",
                   "Hyperbel ohne Punkt bei x = 0" if n < 0 else "durch den Ursprung", z(a), fx(a, n)))


def wurzel():
    kind = R.choice(["sq", "sq", "cb", "pot", "db", "neg"])
    if kind == "sq":
        x = R.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, Fr(1, 4), Fr(9, 4), Fr(49, 100)])
        x = Fr(x)
        r = Fr(int(math.isqrt(x.numerator)), int(math.isqrt(x.denominator)))
        return mcq("Berechne f(%s) für f(x) = x<sup>1/2</sup>." % z(x), z(r), [z(x / 2), z(x * x) if x * x < 10000 else z(r + 1), z(-r)],
                   "x<sup>1/2</sup> = √x: √%s = <b>%s</b>." % (z(x), z(r)))
    if kind == "cb":
        c = R.choice([2, 3, 4, 5, 10])
        x = c ** 3
        s = R.choice([1, -1])
        return mcq("Löse x<sup>3</sup> = %s." % z(s * x), "x = %s" % z(s * c), ["x = %s" % z(-s * c), "x = %s" % z(Fr(s * x, 3)), "x = ±%d" % c],
                   "%s<sup>3</sup> = %s. Bei ungeradem Exponenten gibt es genau eine Lösung: <b>x = %s</b>." % (par(s * c), z(s * x), z(s * c)))
    if kind == "pot":
        m = R.choice([2, 3, 4])
        nm = {2: "√x", 3: "∛x", 4: "∜x"}[m]
        return mcq("Wie schreibt man %s als Potenz?" % nm, "x<sup>1/%d</sup>" % m, ["x<sup>%d</sup>" % m, "x<sup>%s%d</sup>" % (M, m), "%d %s x" % (m, MAL) if m != 2 else "x : 2"],
                   "Die n-te Wurzel ist die Potenz mit Exponent 1/n: <b>x<sup>1/%d</sup></b>." % m)
    if kind == "db":
        return mcq("Welche Definitionsmenge hat f(x) = √x?", "D = ℝ₀⁺ (alle x ≥ 0)", ["D = ℝ", "D = ℝ ∖ {0}", "D = ℝ⁺ (alle x &gt; 0)"],
                   "Aus negativen Zahlen kann man keine Quadratwurzel ziehen, √0 = 0: <b>D = ℝ₀⁺</b>.")
    n = R.choice([-1, -2, -3])
    x = Fr(R.choice([2, 3, 4, 5, 10]))
    v = x ** n
    if v.denominator > 1000:
        return None
    return mcq("Welche Zahl ist %d%s?" % (x, sup(n)), z(v), [z(x * n), z(-x ** (-n)), z(x ** (-n))],
               "%d%s = 1 : %d%s = <b>%s</b>. Ein negativer Exponent macht die Zahl nicht negativ." % (x, sup(n), x, sup(-n), z(v)))


def anwendung():
    kind = R.choice(["gl", "gl", "fl", "vol", "fall", "hyp"])
    if kind == "gl":
        n = R.choice([2, 4, 3, 5])
        c = R.choice([2, 3, 4, 5, 6, 10])
        x = c ** n
        if x > 100000:
            return None
        if n % 2 == 0:
            ans = "x = %d oder x = %s%d" % (c, M, c)
            return mcq("Löse x%s = %s." % (sup(n), num(x)), ans, ["nur x = %d" % c, "x = %s" % num(x // n) if x % n == 0 else "x = %s" % zr(x / n, 1), "keine Lösung"],
                       "%d%s = (%s%d)%s = %s: <b>%s</b>." % (c, sup(n), M, c, sup(n), num(x), ans))
        return mcq("Löse x%s = %s%s." % (sup(n), M, num(x)), "x = %s%d" % (M, c), ["keine Lösung", "x = %d" % c, "x = ±%d" % c],
                   "(%s%d)%s = %s%s. <b>x = %s%d</b>." % (M, c, sup(n), M, num(x), M, c))
    if kind == "fl":
        k = R.choice([2, 3, 4, 5, 10])
        return mcq("Die Seitenlänge eines Quadrats wird mit %d multipliziert. Mit welchem Faktor ändert sich der Flächeninhalt?" % k, "mit %d" % (k * k), ["mit %d" % k, "mit %d" % (2 * k), "mit %d" % (k ** 3)],
                   "A = s<sup>2</sup>: (%d s)<sup>2</sup> = %d s<sup>2</sup>. <b>mit %d</b>" % (k, k * k, k * k))
    if kind == "vol":
        k = R.choice([2, 3, 4, 5])
        return mcq("Die Kantenlänge eines Würfels wird mit %d multipliziert. Mit welchem Faktor ändert sich das Volumen?" % k, "mit %d" % (k ** 3), ["mit %d" % k, "mit %d" % (k * k), "mit %d" % (3 * k)],
                   "V = a<sup>3</sup>: (%d a)<sup>3</sup> = %d a<sup>3</sup>. <b>mit %d</b>" % (k, k ** 3, k ** 3))
    if kind == "fall":
        t = R.choice([1, 2, 3, 4, 5, Fr(3, 2), Fr(5, 2)])
        s = 5 * Fr(t) ** 2
        return mcq("Für den Fallweg gilt näherungsweise s(t) = 5 %s t<sup>2</sup> (s in m, t in s). Wie weit fällt ein Stein in %s s?" % (MAL, z(t)), "%s m" % z(s),
                   ["%s m" % z(10 * Fr(t)), "%s m" % z((5 * Fr(t)) ** 2), "%s m" % z(5 * Fr(t) + 2)],
                   "s = 5 %s %s<sup>2</sup> = 5 %s %s = <b>%s m</b>." % (MAL, z(t), MAL, z(Fr(t) ** 2), z(s)))
    k = R.choice([12, 24, 36, 48, 60])
    x = R.choice([d for d in (2, 3, 4, 6) if k % d == 0])
    return mcq("Ein Rechteck hat den Flächeninhalt %d cm². Für die Breite gilt b(x) = %d %s x<sup>%s1</sup> (x = Länge in cm). Wie breit ist es bei %d cm Länge?" % (k, k, MAL, M, x), "%d cm" % (k // x),
               ["%d cm" % (k * x), "%d cm" % (k - x), "%s cm" % z(Fr(x, k))],
               "b = %d : %d = <b>%d cm</b>. Doppelte Länge, halbe Breite (antiproportional)." % (k, x, k // x))


def main():
    seen = set()
    sets = [
        ("Funktionswerte", mix(R, seen, [(werte, 20)])),
        ("Symmetrie und Verlauf", mix(R, seen, [(eigenschaften, 20)])),
        ("Graphen zuordnen", mix(R, seen, [(graph, 20)])),
        ("Negative Exponenten und Wurzeln", mix(R, seen, [(wurzel, 20)])),
        ("Gleichungen und Anwendungen", mix(R, seen, [(anwendung, 20)])),
    ]
    body = lesson(
        ["Eine <b>Potenzfunktion</b> hat die Form f(x) = a %s x<sup>n</sup>." % MAL,
         "Gerader Exponent: Graph achsensymmetrisch zur y-Achse, durch (−1 | 1) und (1 | 1). Ungerader Exponent: punktsymmetrisch zum Ursprung, durch (−1 | −1) und (1 | 1).",
         "Negativer Exponent: x<sup>−n</sup> = 1 : x<sup>n</sup>. Der Graph ist eine <b>Hyperbel</b>, x = 0 gehört nicht zur Definitionsmenge; die Achsen sind Asymptoten.",
         "Wurzeln sind Potenzen mit Bruch-Exponent: √x = x<sup>1/2</sup>, ∛x = x<sup>1/3</sup>."],
        [example("f(x) = x<sup>4</sup>, f(−2)", ["(−2)<sup>4</sup> = 16"], "16"),
         example("x<sup>4</sup> = 81", ["3<sup>4</sup> = 81 und (−3)<sup>4</sup> = 81"], "x = 3 oder x = −3")],
        [["(−2)<sup>4</sup> = −16", "(−2)<sup>4</sup> = 16"],
         ["2<sup>−2</sup> = −4", "2<sup>−2</sup> = ¼"],
         ["Kante verdoppelt ⇒ Volumen verdoppelt", "Volumen mal 2<sup>3</sup> = 8"]])
    faq = [
        {"q": "Was ist eine Potenzfunktion?", "a": "Eine Funktion f(x) = a · xⁿ, zum Beispiel x², x³ oder x⁻¹."},
        {"q": "Wann ist der Graph symmetrisch zur y-Achse?", "a": "Wenn der Exponent gerade ist, denn dann ist f(−x) = f(x)."},
        {"q": "Wie sieht der Graph von 1/x aus?", "a": "Eine Hyperbel mit zwei Ästen; die x-Achse und die y-Achse sind Asymptoten, x = 0 ist nicht erlaubt."},
        {"q": "Wie viele Lösungen hat x⁴ = 81?", "a": "Zwei: x = 3 und x = −3. Bei ungeradem Exponenten gibt es nur eine Lösung."},
    ]
    make_unit(R, "potenzfunktionen", "F",
              "Die Schülerinnen und Schüler untersuchen Potenzfunktionen mit ganzzahligen Exponenten und Wurzelfunktionen: Symmetrie, gemeinsame Punkte, Definitions- und Wertebereich, Graphen, Gleichungen xⁿ = c und Anwendungen (Zusammenfassung).",
              "Potenzfunktionen",
              "Potenzfunktionen Klasse 10 – Symmetrie, Hyperbeln, Wurzelfunktionen, Arbeitsblätter mit Lösungen",
              "Potenzfunktionen",
              "Potenzfunktionen für Klasse 10: Funktionswerte, gerade und ungerade Exponenten, Symmetrie, Hyperbeln, Wurzelfunktionen, Graphen und Gleichungen xⁿ = c. 100 Aufgaben mit Lösungen, kostenlos.",
              "f(x) = a · xⁿ",
              "n gerade: symmetrisch zur y-Achse. n ungerade: symmetrisch zum Ursprung.",
              body, faq, sets, 4, grade="klasse-10")


if __name__ == "__main__":
    main()
