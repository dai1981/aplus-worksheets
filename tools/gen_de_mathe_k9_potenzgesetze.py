# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Potenzgesetze（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k9_potenzgesetze.py
Potenzen mit negativen Exponenten und Exponent 0, Multiplizieren und Dividieren bei gleicher Basis, Potenzieren von Potenzen,
gleiche Exponenten, Terme mit Variablen vereinfachen, Sachaufgaben (Verdopplung, Speichergrößen, Zehnerpotenzen).
Fehler: Exponenten multipliziert statt addiert, Basen multipliziert, a⁻² als negative Zahl, (a³)² = a⁵.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import bh, dz
from de_k9 import mcq, zahl

R = random.Random(49901)
G = ":"


def sup(n):
    return "<sup>%s</sup>" % (("−%d" % -n) if n < 0 else str(n))


def pw(b, n):
    b = str(b)
    if b.startswith("−") or "/" in b:
        b = "(%s)" % b
    return b + sup(n)


def negativ():
    kind = R.choice(["wert", "wert", "null", "bruch", "schreib"])
    if kind == "wert":
        b, n = R.choice([(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 3), (4, 2), (5, 2), (5, 3), (10, 2), (10, 3), (6, 2), (7, 2)])
        v = Fr(1, b ** n)
        return mcq("Berechne %s." % pw(b, -n), bh(v), [dz(-(b ** n)), dz(-b * n), bh(Fr(1, b * n)) if b * n != b ** n else bh(Fr(1, b ** n + 1))],
                   "%s = 1 %s %s = <b>%s</b>." % (pw(b, -n), G, pw(b, n), bh(v)))
    if kind == "null":
        b = R.choice([3, 7, 12, 25, "a", "x"])
        return mcq("Berechne bzw. vereinfache %s%s." % (pw(b, 0), " (%s ≠ 0)" % b if b in ("a", "x") else ""), "1", ["0", str(b), "nicht definiert"],
                   "Jede Zahl außer 0 hoch 0 ergibt <b>1</b>.")
    if kind == "bruch":
        z, nn = R.choice([(1, 2), (2, 3), (3, 4), (1, 5), (2, 5), (3, 2)])
        n = R.choice([1, 2, 3])
        v = Fr(nn, z) ** n
        return mcq("Berechne (%s)%s." % (bh(Fr(z, nn)), sup(-n)), zahl(v), [zahl(-(Fr(z, nn) ** n)), zahl(Fr(z, nn) ** n), zahl(Fr(nn, z) * n) if Fr(nn, z) * n != v else zahl(v + 1)],
                   "Negativer Exponent: Kehrwert nehmen. (%s)%s = <b>%s</b>." % (bh(Fr(nn, z)), sup(n), zahl(v)))
    b = R.choice([2, 3, 5, 10, "x", "a"])
    n = R.randint(2, 5)
    if isinstance(b, int):
        return mcq("Schreibe 1 %s %s als Potenz mit negativem Exponenten." % (G, num(b ** n)), pw(b, -n), [pw(b, n), pw(b, -n + 1), "−" + pw(b, n)],
                   "1 %s %s = <b>%s</b>." % (G, pw(b, n), pw(b, -n)))
    return mcq("Schreibe %s ohne negativen Exponenten." % pw(b, -n), "<span class='fr'><span class='fn'>1</span><span class='fd'>%s</span></span>" % pw(b, n),
               ["−" + pw(b, n), "<span class='fr'><span class='fn'>1</span><span class='fd'>%s</span></span>" % pw(b, -n), "−%d%s" % (n, b)],
               "a%s = 1 %s a%s. <b>1 %s %s</b>" % (sup(-n), G, sup(n), G, pw(b, n)))


def gleiche_basis():
    v = R.choice(["2", "3", "10", "x", "a", "y"])
    m, n = R.randint(-4, 7), R.randint(-4, 7)
    if m in (0, 1) or n in (0, 1):
        return None
    kind = R.choice(["mal", "mal", "geteilt"])
    if kind == "mal":
        e = m + n
        return mcq("Schreibe als eine Potenz: %s %s %s" % (pw(v, m), MAL, pw(v, n)), pw(v, e) if e else "1", [pw(v, m * n) if m * n != e else pw(v, e + 1), pw(str(int(v) ** 2), e) if v.isdigit() and int(v) ** 2 < 200 else pw(v, m - n) if m - n != e else pw(v, e - 1), pw(v, m - n) if m - n != e and v.isdigit() else pw(v, e + 2)],
                   "Gleiche Basis: Exponenten addieren, %s + %s = %s. <b>%s</b>" % (dz(m), par_(n), dz(e), pw(v, e) if e else "1"))
    e = m - n
    return mcq("Schreibe als eine Potenz: %s %s %s" % (pw(v, m), G, pw(v, n)), pw(v, e) if e else "1", [pw(v, m + n) if m + n != e else pw(v, e + 1), pw(v, Fr(m, n)) if n and Fr(m, n).denominator == 1 and Fr(m, n) != e else pw(v, e - 1), "1" if e else pw(v, 1)],
               "Gleiche Basis: Exponenten subtrahieren, %s − %s = %s. <b>%s</b>" % (dz(m), par_(n), dz(e), pw(v, e) if e else "1"))


def par_(n):
    return "(%s)" % dz(n) if n < 0 else dz(n)


def potenz_potenz():
    kind = R.choice(["pp", "pp", "exp", "zahl"])
    if kind == "pp":
        v = R.choice(["x", "a", "2", "3", "b"])
        m, n = R.randint(-3, 5), R.randint(2, 4)
        if m in (0, 1):
            return None
        return mcq("Vereinfache: (%s)%s" % (pw(v, m), sup(n)), pw(v, m * n), [pw(v, m + n), pw(v, m ** n) if m ** n != m * n else pw(v, m * n + 1), pw(v, m * n - 1)],
                   "Potenz einer Potenz: Exponenten multiplizieren, %s %s %d = %s. <b>%s</b>" % (dz(m), MAL, n, dz(m * n), pw(v, m * n)))
    if kind == "exp":
        k = R.randint(2, 5)
        a, b = R.sample(["a", "b", "x", "y"], 2)
        n = R.randint(2, 4)
        return mcq("Vereinfache: (%d%s)%s" % (k, a + b, sup(n)), "%s%s%s%s" % (num(k ** n), a, sup(n), b + sup(n)),
                   ["%d%s%s%s" % (k, a, sup(n), b + sup(n)), "%d%s%s%s" % (k * n, a, sup(n), b + sup(n)), "%s%s%s" % (num(k ** n), a + b, "")],
                   "Jeder Faktor wird potenziert: %d%s = %s. <b>%s%s%s%s</b>" % (k, sup(n), num(k ** n), num(k ** n), a, sup(n), b + sup(n)))
    a, b = R.choice([(2, 5), (4, 25), (8, 125), (2, 50), (5, 20), (4, 5), (25, 4), (3, 4)])
    n = R.randint(2, 4)
    if (a * b) ** n > 10 ** 7:
        return None
    return mcq("Berechne geschickt: %s %s %s" % (pw(a, n), MAL, pw(b, n)), num((a * b) ** n), [num((a + b) ** n), num(a ** n + b ** n), num((a * b) ** (2 * n)) if (a * b) ** (2 * n) < 10 ** 9 else num((a * b) ** n * 10)],
               "Gleiche Exponenten: (%d %s %d)%s = %s = <b>%s</b>." % (a, MAL, b, sup(n), pw(a * b, n), num((a * b) ** n)))


def terme():
    kind = R.choice(["koef", "koef", "bruch", "mix", "minus"])
    p, q = R.randint(2, 9), R.randint(2, 9)
    m, n = R.randint(2, 6), R.randint(2, 6)
    if kind == "koef":
        return mcq("Vereinfache: %dx%s %s %dx%s" % (p, sup(m), MAL, q, sup(n)), "%dx%s" % (p * q, sup(m + n)), ["%dx%s" % (p + q, sup(m + n)), "%dx%s" % (p * q, sup(m * n)), "%dx%s" % (p * q, sup(m + n + 1))],
                   "Zahlen multiplizieren (%d), Exponenten addieren (%d): <b>%dx%s</b>." % (p * q, m + n, p * q, sup(m + n)))
    if kind == "bruch":
        if m <= n:
            m, n = n + R.randint(1, 3), m
        k = R.randint(2, 6)
        return mcq("Vereinfache: %dx%s %s %dx%s" % (k * p, sup(m), G, p, sup(n)), "%dx%s" % (k, sup(m - n)) if m - n != 1 else "%dx" % k, ["%dx%s" % (k, sup(Fr(m, n))) if Fr(m, n).denominator == 1 else "%dx%s" % (k, sup(m + n)), "%dx%s" % (k * p, sup(m - n)), "%dx%s" % (k - p if k > p else k + p, sup(m - n))],
                   "%d %s %d = %d, Exponenten subtrahieren: %d − %d = %d. <b>%s</b>" % (k * p, G, p, k, m, n, m - n, "%dx%s" % (k, sup(m - n)) if m - n != 1 else "%dx" % k))
    if kind == "mix":
        return mcq("Vereinfache: a%s %s b%s %s a %s b%s" % (sup(m), MAL, sup(n), MAL, MAL, sup(2)), "a%sb%s" % (sup(m + 1), sup(n + 2)),
                   ["a%sb%s" % (sup(m), sup(n + 2)), "(ab)%s" % sup(m + n + 3), "a%sb%s" % (sup(m + 1), sup(2 * n))],
                   "Nur gleiche Basen zusammenfassen: a%s %s a = a%s, b%s %s b² = b%s. <b>a%sb%s</b>" % (sup(m), MAL, sup(m + 1), sup(n), MAL, sup(n + 2), sup(m + 1), sup(n + 2)))
    return mcq("Vereinfache: x%s %s x%s" % (sup(m), MAL, sup(-n)), ("x%s" % sup(m - n)) if m - n not in (0, 1) else ("1" if m == n else "x"),
               ["x%s" % sup(-m * n), "x%s" % sup(m + n), "−x%s" % sup(m - n) if m != n else "0"],
               "%d + (−%d) = %s. <b>%s</b>" % (m, n, dz(m - n), ("x%s" % sup(m - n)) if m - n not in (0, 1) else ("1" if m == n else "x")))


def sache():
    kind = R.choice(["bakt", "byte", "papier", "zehn", "zehn2"])
    if kind == "bakt":
        n0 = R.choice([10, 100, 50, 20])
        h = R.choice([3, 4, 5, 6, 8, 10])
        return mcq("Eine Bakterienkultur verdoppelt sich jede Stunde. Am Anfang sind es %d Bakterien. Wie viele sind es nach %d Stunden?" % (n0, h), num(n0 * 2 ** h),
                   [num(n0 * 2 * h), num(n0 + 2 ** h), num(n0 * 2 ** (h - 1))], "%d %s 2%s = %d %s %s = <b>%s</b>." % (n0, MAL, sup(h), n0, MAL, num(2 ** h), num(n0 * 2 ** h)))
    if kind == "byte":
        a, b = R.choice([(10, 10), (20, 10), (30, 20), (30, 10), (20, 3), (10, 3)])
        if a <= b:
            return None
        return mcq("Ein Datenspeicher fasst 2%s Byte, eine Datei hat 2%s Byte. Wie oft passt die Datei hinein?" % (sup(a), sup(b)), "2%s-mal" % sup(a - b), ["2%s-mal" % sup(Fr(a, b)) if Fr(a, b).denominator == 1 else "2%s-mal" % sup(a + b), "%d-mal" % (a - b), "2%s-mal" % sup(a + b)],
                   "2%s %s 2%s = <b>2%s</b>." % (sup(a), G, sup(b), sup(a - b)))
    if kind == "papier":
        n = R.choice([5, 6, 7, 8, 10])
        return mcq("Ein Blatt Papier ist 0,1 mm dick. Wie dick ist der Stapel, wenn man es %d-mal faltet?" % n, "%s mm" % dz(Fr(2 ** n, 10)), ["%s mm" % dz(Fr(2 * n, 10)), "%s mm" % dz(Fr(n ** 2, 10)), "%s mm" % dz(Fr(2 ** (n - 1), 10))],
                   "Jedes Falten verdoppelt: 0,1 %s 2%s = 0,1 %s %d = <b>%s mm</b>." % (MAL, sup(n), MAL, 2 ** n, dz(Fr(2 ** n, 10))))
    if kind == "zehn":
        a, b = R.randint(-6, 9), R.randint(-6, 9)
        if a == b or 0 in (a, b):
            return None
        big, small = max(a, b), min(a, b)
        return mcq("Wie oft ist 10%s größer als 10%s?" % (sup(big), sup(small)), "%s-mal" % num(10 ** (big - small)) if big - small <= 6 else "10%s-mal" % sup(big - small),
                   ["%d-mal" % (big - small), ("%s-mal" % num(10 ** (big + small))) if 0 < big + small <= 6 else "10%s-mal" % sup(big + small) if big + small != big - small else "100-mal", "10%s-mal" % sup(big * small) if big * small != big - small else "2-mal"],
                   "10%s %s 10%s = 10%s. <b>%s</b>" % (sup(big), G, sup(small), sup(big - small), ("%s-mal" % num(10 ** (big - small))) if big - small <= 6 else "10%s-mal" % sup(big - small)))
    m = R.randint(2, 9)
    e = R.randint(3, 9)
    k = R.randint(2, 6)
    return mcq("Ein Land hat %d %s 10%s Einwohner. Jeder verbraucht im Jahr etwa %d %s 10%s Liter Wasser. Wie viel ist das zusammen?" % (m, MAL, sup(e), k, MAL, sup(2)),
               "%s %s 10%s Liter" % (dz(Fr(m * k, 10)) if m * k >= 10 else dz(m * k), MAL, sup(e + 3 if m * k >= 10 else e + 2)),
               ["%s %s 10%s Liter" % (dz(Fr(m * k, 10)) if m * k >= 10 else dz(m * k), MAL, sup(2 * e if 2 * e != (e + 3 if m * k >= 10 else e + 2) else e + 4)), "%d %s 10%s Liter" % (m + k, MAL, sup(e + 2)), "%s %s 10%s Liter" % (dz(Fr(m * k, 10)) if m * k >= 10 else dz(m * k), MAL, sup(e))],
               "%d %s %d = %d, Exponenten %d + 2 = %d. <b>%s %s 10%s Liter</b>" % (m, MAL, k, m * k, e, e + 2, dz(Fr(m * k, 10)) if m * k >= 10 else dz(m * k), MAL, sup(e + 3 if m * k >= 10 else e + 2)))


def main():
    seen = set()
    sets = [
        ("Negative Exponenten", mix(R, seen, [(negativ, 20)])),
        ("Gleiche Basis", mix(R, seen, [(gleiche_basis, 20)])),
        ("Potenzen potenzieren", mix(R, seen, [(potenz_potenz, 20)])),
        ("Terme vereinfachen", mix(R, seen, [(terme, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Gleiche Basis</b>: a<sup>m</sup> %s a<sup>n</sup> = a<sup>m+n</sup> und a<sup>m</sup> %s a<sup>n</sup> = a<sup>m−n</sup>." % (MAL, G),
         "<b>Gleiche Exponenten</b>: a<sup>n</sup> %s b<sup>n</sup> = (a %s b)<sup>n</sup>." % (MAL, MAL),
         "<b>Potenz einer Potenz</b>: (a<sup>m</sup>)<sup>n</sup> = a<sup>m%sn</sup>." % MAL,
         "<b>Negative Exponenten</b>: a<sup>−n</sup> = 1 %s a<sup>n</sup>, und a<sup>0</sup> = 1 (a ≠ 0)." % G],
        [example("x<sup>5</sup> %s x<sup>3</sup>" % MAL, ["5 + 3 = 8"], "x<sup>8</sup>"),
         example("(2<sup>3</sup>)<sup>2</sup>", ["3 %s 2 = 6" % MAL], "2<sup>6</sup> = 64"),
         example("5<sup>−2</sup>", ["1 %s 5<sup>2</sup>" % G], "1/25")],
        [["x<sup>3</sup> %s x<sup>4</sup> = x<sup>12</sup>" % MAL, "Exponenten addieren: x<sup>7</sup>"],
         ["2<sup>−3</sup> = −8", "2<sup>−3</sup> = 1/8 (positiv)"],
         ["(x<sup>3</sup>)<sup>2</sup> = x<sup>5</sup>", "Exponenten multiplizieren: x<sup>6</sup>"]])
    faq = [
        {"q": "Welche Potenzgesetze gibt es?", "a": "a^m · a^n = a^(m+n), a^m : a^n = a^(m−n), (a^m)^n = a^(m·n) und a^n · b^n = (a·b)^n."},
        {"q": "Was bedeutet ein negativer Exponent?", "a": "a^(−n) = 1 : a^n. Zum Beispiel 2^(−3) = 1/8. Das Ergebnis ist nicht negativ."},
        {"q": "Warum ist a^0 = 1?", "a": "a^n : a^n = a^(n−n) = a^0, und eine Zahl durch sich selbst ergibt 1."},
        {"q": "Darf ich x² · y³ zusammenfassen?", "a": "Nein, nur Potenzen mit gleicher Basis oder gleichem Exponenten lassen sich zusammenfassen."},
    ]
    make_unit(R, "potenzgesetze", "Z",
              "Die Schülerinnen und Schüler rechnen mit Potenzen mit ganzzahligen Exponenten, wenden die Potenzgesetze an und vereinfachen Terme mit Potenzen (Zusammenfassung).",
              "Potenzgesetze",
              "Potenzgesetze Klasse 9 – negative Exponenten, Arbeitsblätter mit Lösungen",
              "Potenzgesetze",
              "Potenzgesetze für Klasse 9: negative Exponenten, gleiche Basis, gleiche Exponenten, Potenzen potenzieren, Terme vereinfachen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "aᵐ · aⁿ = aᵐ⁺ⁿ",
              "(aᵐ)ⁿ = aᵐ·ⁿ und a⁻ⁿ = 1 : aⁿ",
              body, faq, sets, 1, grade="klasse-9")


if __name__ == "__main__":
    main()
