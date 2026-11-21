# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Logarithmus（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k10_logarithmus.py
log_b(x) als Exponent, Potenz- und Logarithmusschreibweise, lg (Zehnerlogarithmus), Logarithmengesetze,
Exponentialgleichungen b^x = c (genau und mit dem Taschenrechner), Sachaufgaben (Verdopplungszeit, Laufzeit).
Fehler: log₂ 8 = 4 (geteilt statt Exponent), log(u + v) = log u + log v, log_b 1 = 1, b^x = c ⇒ x = c : b.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import bh, dz, endlich
from de_k10 import mcq, zr

R = random.Random(50003)
M = "−"


def lg_(b):
    return "lg" if b == 10 else "log<sub>%d</sub>" % b


def L(b, x):
    return "%s %s" % (lg_(b), x)


def z(v):
    v = Fr(v)
    if v < 0:
        return M + z(-v)
    return dz(v) if endlich(v) else bh(v)


def sup(n):
    return "<sup>%s</sup>" % ((M + str(-n)) if n < 0 else str(n))


BASES = [2, 3, 4, 5, 10]


def potzahl(b, k):
    v = Fr(b) ** k
    if k < 0 and b != 10 and v.denominator > 4:
        return bh(v)
    return z(v)


def berechnen():
    b = R.choice(BASES)
    hi = {2: 7, 3: 5, 4: 4, 5: 4, 10: 6}[b]
    k = R.randint(-3, hi)
    if k == 1 and R.random() < 0.6:
        return None
    x = Fr(b) ** k
    xs = potzahl(b, k)
    w = [z(x / b) if k > 0 and x / b != k else z(k + 1), z(-k) if k else "1", z(k - 1) if k > 1 else z(k + 2)]
    if k == 0:
        w = ["1", z(b), "nicht definiert"]
    e = "%s%s = %s, also %s = <b>%s</b>." % (b, sup(k), xs, L(b, xs), z(k))
    if k == 0:
        e += " Jede Basis hoch 0 ergibt 1."
    return mcq("Berechne %s." % L(b, xs), z(k), w, e)


def umschreiben():
    b = R.choice(BASES + [6, 7])
    k = R.randint(-2, 4)
    if k in (0, 1):
        return None
    xs = potzahl(b, k)
    if R.random() < 0.5:
        return mcq("Welche Potenz-Schreibweise gehört zu %s = %s?" % (L(b, xs), z(k)), "%d%s = %s" % (b, sup(k), xs),
                   ["%s%s = %d" % (xs, sup(k), b) if k > 0 else "%s<sup>%d</sup> = %s" % (z(k), b, xs), "%d %s %s = %s" % (b, MAL, z(k), xs), "%s%s = %s" % (z(k), sup(b), xs)],
                   "log<sub>b</sub> x = y bedeutet b<sup>y</sup> = x: <b>%d%s = %s</b>." % (b, sup(k), xs))
    return mcq("Schreibe %d%s = %s als Logarithmus." % (b, sup(k), xs), "%s = %s" % (L(b, xs), z(k)),
               ["%s = %s" % (L(b, z(k)), xs) if k > 0 else "%s = %s" % (lg_(b) + " " + z(k), xs), "log<sub>%s</sub> %d = %s" % (xs, b, z(k)), "%s = %s" % (L(b, xs), xs)],
               "Der Exponent ist der Logarithmus: <b>%s = %s</b>." % (L(b, xs), z(k)))


def gesetze():
    kind = R.choice(["prod", "quot", "pot", "falsch", "lg"])
    if kind == "prod":
        b = R.choice([2, 3, 4, 6, 10])
        u, v = R.sample([Fr(b) ** i for i in range(1, 5)] + [Fr(1, b)], 2)
        s = math.log(u * v, b)
        r = round(s)
        if abs(s - r) > 1e-9:
            return None
        return mcq("Berechne %s + %s." % (L(b, z(u)), L(b, z(v))), z(r),
                   [z(round(math.log(u, b)) * round(math.log(v, b))), z(u * v), L(b, z(u + v))],
                   "Produktregel: %s + %s = %s = <b>%s</b>." % (L(b, z(u)), L(b, z(v)), L(b, z(u * v)), z(r)))
    if kind == "quot":
        b = R.choice([2, 3, 5, 10])
        k1, k2 = R.sample(range(1, 7 if b == 2 else 5), 2)
        c = R.choice([2, 3, 5, 6, 7])
        u, v = c * b ** k1, c * b ** k2
        if max(u, v) > 100000:
            return None
        return mcq("Berechne %s %s %s." % (L(b, num(u)), M, L(b, num(v))), z(k1 - k2),
                   [z(Fr(k1, k2)) if k2 != 1 and Fr(k1, k2) != k1 - k2 else z(k1 + k2), z(Fr(u, v)) if Fr(u, v) != k1 - k2 else z(k2 - k1), L(b, num(u - v)) if u > v else z(k2 - k1)],
                   "Quotientenregel: %s = %s = <b>%s</b>." % (L(b, "(%s : %s)" % (num(u), num(v))), L(b, z(Fr(u, v))), z(k1 - k2)))
    if kind == "pot":
        b = R.choice([2, 3, 5, 10])
        k = R.randint(2, 3 if b != 2 else 4)
        r = R.randint(2, 6)
        return mcq("Vereinfache %s mit der Potenzregel und berechne." % L(b, "(%d<sup>%d</sup>)<sup>%d</sup>" % (b, k, r)), num(k * r),
                   [num(k + r), num(k ** r), num(r)], "%s = %d %s %s = %d %s %d = <b>%d</b>." % (L(b, "(%d<sup>%d</sup>)<sup>%d</sup>" % (b, k, r)), r, MAL, L(b, "%d<sup>%d</sup>" % (b, k)), r, MAL, k, k * r))
    if kind == "falsch":
        a, c = R.sample(["u", "v", "a", "x"], 2)
        good = [("log(%s %s %s) = log %s + log %s" % (a, MAL, c, a, c)), ("log(%s : %s) = log %s − log %s" % (a, c, a, c)), ("log(%s<sup>3</sup>) = 3 %s log %s" % (a, MAL, a)), ("log 1 = 0")]
        bad = R.choice(["log(%s + %s) = log %s + log %s" % (a, c, a, c), "log(%s %s %s) = log %s %s log %s" % (a, MAL, c, a, MAL, c), "log(%s<sup>3</sup>) = (log %s)<sup>3</sup>" % (a, a), "log(%s − %s) = log %s − log %s" % (a, c, a, c)])
        return mcq("Welche Gleichung ist <b>falsch</b> (für positive %s und %s)?" % (a, c), bad, R.sample(good, 3),
                   "<b>%s</b> ist falsch. Für Summen und Differenzen im Logarithmus gibt es keine Regel; die Gesetze gelten für Produkte, Quotienten und Potenzen." % bad)
    p = R.choice([2, 3, 4, 5, 6, 7, 8])
    k = R.randint(1, 3)
    v = p * 10 ** k
    return mcq("Es ist lg %d ≈ %s. Wie groß ist lg %s?" % (p, zr(math.log10(p), 3), num(v)), "≈ %s" % zr(math.log10(v), 3),
               ["≈ %s" % zr(math.log10(p) * 10 ** k, 3), "≈ %s" % zr(math.log10(p) * k, 3), "≈ %s" % zr(math.log10(p) + 10 ** k, 3)],
               "lg %s = lg %d + lg 10<sup>%d</sup> ≈ %s + %d = <b>%s</b>." % (num(v), p, k, zr(math.log10(p), 3), k, zr(math.log10(v), 3)))


def gleichung():
    kind = R.choice(["genau", "genau", "a", "tr", "tr"])
    if kind == "genau":
        b = R.choice([2, 3, 4, 5, 10])
        k = R.randint(-3, {2: 8, 3: 6, 4: 4, 5: 4, 10: 6}[b])
        if k in (0, 1):
            return None
        c = Fr(b) ** k
        return mcq("Löse %d<sup>x</sup> = %s." % (b, potzahl(b, k)), "x = %s" % z(k),
                   ["x = %s" % z(c / b) if c / b != k else "x = %s" % z(k + 1), "x = %s" % z(-k), "x = %s" % z(k + 1) if c / b == k else "x = %s" % z(k - 1)],
                   "%s = %d%s, also <b>x = %s</b>." % (potzahl(b, k), b, sup(k), z(k)))
    if kind == "a":
        a = R.choice([2, 3, 4, 5, 6])
        b = R.choice([2, 3, 5])
        k = R.randint(2, 5)
        c = a * b ** k
        return mcq("Löse %d %s %d<sup>x</sup> = %s." % (a, MAL, b, num(c)), "x = %d" % k,
                   ["x = %s" % zr(math.log(c, a * b), 2), "x = %s" % z(Fr(c, a * b)), "x = %d" % (k + 1)],
                   "Erst durch %d teilen: %d<sup>x</sup> = %s = %d%s, also <b>x = %d</b>. (Nicht (%d %s %d)<sup>x</sup> rechnen.)" % (a, b, num(b ** k), b, sup(k), k, a, MAL, b))
    b = R.choice([2, 3, 5, 7, Fr(3, 2), Fr(11, 10), Fr(105, 100), Fr(12, 10)])
    c = R.choice([5, 10, 20, 50, 100, 3, 7])
    x = math.log(c) / math.log(b)
    if x > 80 or abs(x - round(x)) < 0.02:
        return None
    return mcq("Löse %s<sup>x</sup> = %d mit dem Taschenrechner (auf zwei Nachkommastellen)." % (z(b), c), "x ≈ %s" % zr(x, 2),
               ["x ≈ %s" % zr(c / float(b), 2), "x ≈ %s" % zr(math.log10(c) * float(b), 2), "x ≈ %s" % zr(math.log10(float(b)) / math.log10(c), 2)],
               "x = lg %d : lg %s ≈ <b>%s</b>." % (c, z(b), zr(x, 2)))


def sach():
    kind = R.choice(["verdopp", "kapital", "halb", "bakt", "abnahme"])
    if kind == "verdopp":
        p = R.choice([1, 2, 3, 4, 6, 8, 9])
        x = math.log(2) / math.log(1 + p / 100)
        return mcq("Wie lange dauert es, bis sich ein Kapital bei %d %% Zinseszins verdoppelt hat (auf eine Nachkommastelle)?" % p, "≈ %s Jahre" % zr(x, 1),
                   ["≈ %s Jahre" % zr(100 / p, 1), "≈ %s Jahre" % zr(2 / (1 + p / 100), 1), "≈ %s Jahre" % zr(x / 2, 1)],
                   "1,%02d<sup>n</sup> = 2 ⇒ n = lg 2 : lg 1,%02d ≈ <b>%s Jahre</b>." % (p, p, zr(x, 1)))
    if kind == "kapital":
        K = R.choice([1000, 2000, 5000, 4000])
        Z = K * R.choice([Fr(3, 2), Fr(5, 4), Fr(3), Fr(8, 5)])
        p = R.choice([2, 3, 4, 5])
        x = math.log(float(Z / K)) / math.log(1 + p / 100)
        n = math.ceil(x)
        return mcq("%s € werden zu %d %% angelegt. Nach wie vielen vollen Jahren sind es mindestens %s €?" % (num(K), p, num(int(Z))), "nach %d Jahren" % n,
                   ["nach %d Jahren" % math.ceil((Z / K - 1) * 100 / p), "nach %d Jahren" % (n - 1), "nach %d Jahren" % (n + 2)],
                   "1,%02d<sup>n</sup> = %s ⇒ n = lg %s : lg 1,%02d ≈ %s, also <b>nach %d Jahren</b>." % (p, z(Z / K), z(Z / K), p, zr(x, 2), n))
    if kind == "halb":
        p = R.choice([5, 10, 15, 20, 25, 30])
        x = math.log(0.5) / math.log(1 - p / 100)
        return mcq("Ein Stoff nimmt jede Stunde um %d %% ab. Wie groß ist die Halbwertszeit (auf eine Nachkommastelle)?" % p, "≈ %s Stunden" % zr(x, 1),
                   ["≈ %s Stunden" % zr(50 / p, 1), "≈ %s Stunden" % zr(math.log(0.5) / math.log(1 + p / 100) * -1, 1), "≈ %s Stunden" % zr(x * 2, 1)],
                   "%s<sup>t</sup> = 0,5 ⇒ t = lg 0,5 : lg %s ≈ <b>%s Stunden</b>." % (z(Fr(100 - p, 100)), z(Fr(100 - p, 100)), zr(x, 1)))
    if kind == "bakt":
        n0 = R.choice([100, 200, 500, 1000])
        f = R.choice([2, 3])
        T = R.choice([1, 2, 3, 4])
        g = R.choice([10, 50, 100, 1000])
        x = math.log(g) / math.log(f) * T
        if abs(x - round(x)) < 0.05:
            return None
        wort = "verdoppelt" if f == 2 else "verdreifacht"
        return mcq("%s Bakterien; ihre Zahl %s sich alle %d %s. Nach welcher Zeit sind es %s (auf eine Nachkommastelle)?" % (num(n0), wort, T, "Stunde" if T == 1 else "Stunden", num(n0 * g)),
                   "≈ %s Stunden" % zr(x, 1), ["≈ %s Stunden" % zr(g / f * T, 1), "≈ %s Stunden" % zr(math.log(g) / math.log(f), 1) if T != 1 else "≈ %s Stunden" % zr(x + 2, 1), "≈ %s Stunden" % zr(math.log10(g) * T, 1)],
                   "%d<sup>n</sup> = %s ⇒ n = lg %s : lg %d ≈ %s Schritte zu je %d h ⇒ <b>%s Stunden</b>." % (f, num(g), num(g), f, zr(x / T, 2), T, zr(x, 1)))
    W = R.choice([20000, 30000, 25000])
    p = R.choice([10, 15, 20])
    Z = R.choice([10000, 5000, 8000])
    x = math.log(Z / W) / math.log(1 - p / 100)
    n = math.ceil(x)
    return mcq("Ein Auto (%s €) verliert jährlich %d %% an Wert. Nach wie vielen vollen Jahren ist es weniger als %s € wert?" % (num(W), p, num(Z)), "nach %d Jahren" % n,
               ["nach %d Jahren" % math.ceil((1 - Z / W) * 100 / p), "nach %d Jahren" % (n - 1), "nach %d Jahren" % (n + 2)],
               "%s<sup>n</sup> &lt; %s ⇒ n &gt; lg %s : lg %s ≈ %s, also <b>nach %d Jahren</b>." % (z(Fr(100 - p, 100)), z(Fr(Z, W)), z(Fr(Z, W)), z(Fr(100 - p, 100)), zr(x, 2), n))


def main():
    seen = set()
    sets = [
        ("Logarithmen berechnen", mix(R, seen, [(berechnen, 20)])),
        ("Potenz und Logarithmus", mix(R, seen, [(umschreiben, 12), (berechnen, 8)])),
        ("Logarithmengesetze", mix(R, seen, [(gesetze, 20)])),
        ("Exponentialgleichungen", mix(R, seen, [(gleichung, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sach, 20)])),
    ]
    body = lesson(
        ["Der <b>Logarithmus</b> log<sub>b</sub> x ist der Exponent, mit dem man b potenzieren muss, um x zu erhalten: log<sub>b</sub> x = y ⇔ b<sup>y</sup> = x.",
         "lg x ist der Zehnerlogarithmus (Basis 10). Es gilt immer log<sub>b</sub> 1 = 0 und log<sub>b</sub> b = 1.",
         "Gesetze: log(u %s v) = log u + log v, log(u : v) = log u − log v, log(u<sup>r</sup>) = r %s log u." % (MAL, MAL),
         "Exponentialgleichung b<sup>x</sup> = c: x = log<sub>b</sub> c = lg c : lg b."],
        [example("log<sub>2</sub> 32", ["2<sup>5</sup> = 32"], "5"),
         example("1,05<sup>x</sup> = 2", ["x = lg 2 : lg 1,05"], "x ≈ 14,21")],
        [["log<sub>2</sub> 8 = 8 : 2 = 4", "2<sup>3</sup> = 8, also 3"],
         ["log(u + v) = log u + log v", "Die Regel gilt nur für Produkte"],
         ["3 %s 2<sup>x</sup> = 48 ⇒ 6<sup>x</sup> = 48" % MAL, "Erst durch 3 teilen: 2<sup>x</sup> = 16"]])
    faq = [
        {"q": "Was ist ein Logarithmus?", "a": "Der Exponent: log₂ 8 = 3, weil 2³ = 8."},
        {"q": "Was bedeutet lg?", "a": "lg ist der Logarithmus zur Basis 10: lg 1000 = 3."},
        {"q": "Wie löse ich 1,05^x = 2?", "a": "Logarithmieren: x = lg 2 : lg 1,05 ≈ 14,21."},
        {"q": "Gilt log(u + v) = log u + log v?", "a": "Nein. Die Logarithmengesetze gelten für Produkte, Quotienten und Potenzen, nicht für Summen."},
    ]
    make_unit(R, "logarithmus", "Z",
              "Die Schülerinnen und Schüler verstehen den Logarithmus als Umkehrung des Potenzierens, wenden die Logarithmengesetze an und lösen Exponentialgleichungen, auch in Sachzusammenhängen (Zusammenfassung).",
              "Logarithmus",
              "Logarithmus Klasse 10 – Logarithmengesetze, Exponentialgleichungen, Arbeitsblätter mit Lösungen",
              "Logarithmus",
              "Logarithmus für Klasse 10: Logarithmen berechnen, Potenz- und Logarithmusschreibweise, Logarithmengesetze, Exponentialgleichungen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "log_b x = y ⇔ bʸ = x",
              "Der Logarithmus ist der gesuchte Exponent.",
              body, faq, sets, 3, grade="klasse-10")


if __name__ == "__main__":
    main()
