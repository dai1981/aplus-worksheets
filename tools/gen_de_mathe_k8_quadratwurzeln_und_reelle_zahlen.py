# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Quadratwurzeln und reelle Zahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k8_quadratwurzeln_und_reelle_zahlen.py
Quadratwurzeln aus Quadratzahlen, Dezimalzahlen und Brüchen, Kubikwurzeln, Wurzeln abschätzen (zwischen welchen ganzen Zahlen),
rationale und irrationale Zahlen, Zahlenmengen ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ, Sachaufgaben (Seitenlänge eines Quadrats).
Fehler: √49 = 24,5 (halbiert), √0,9 = 0,3, √(a + b) = √a + √b, jede Wurzel für irrational gehalten.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import bh, dz
from de_k8 import mcq, zk

R = random.Random(49802)
W = "√"


def wz(x):
    return "%s%s" % (W, x)


def ganz():
    kind = R.choice(["q", "q", "k", "umk", "summe"])
    if kind == "q":
        n = R.randint(4, 25)
        return mcq("Berechne %s." % wz(num(n * n)), str(n), [dz(Fr(n * n, 2)), str(n * n // 10) if n * n >= 100 and n * n // 10 != n else str(n + 1), str(n - 1)],
                   "%d %s %d = %s, also <b>%s = %d</b>." % (n, MAL, n, num(n * n), wz(num(n * n)), n))
    if kind == "k":
        n = R.randint(2, 10)
        return mcq("Berechne <sup>3</sup>%s." % wz(num(n ** 3)), str(n), [dz(Fr(n ** 3, 3)) if (Fr(n ** 3, 3) * 100).denominator == 1 else str(n + 1), str(int(round(math.sqrt(n ** 3)))) if int(round(math.sqrt(n ** 3))) != n else str(n + 2), str(n * n)],
                   "%d %s %d %s %d = %s: <b>%d</b>." % (n, MAL, n, MAL, n, num(n ** 3), n))
    if kind == "umk":
        n = R.randint(3, 15)
        return mcq("Welche Zahl ergibt quadriert %s?" % num(n * n), "%d und −%d" % (n, n), ["nur %d" % n, "nur −%d" % n, "%s und −%s" % (dz(Fr(n * n, 2)), dz(Fr(n * n, 2)))],
                   "%d<sup>2</sup> = %s und (−%d)<sup>2</sup> = %s. Die Wurzel %s ist aber nur die positive Zahl %d. <b>%d und −%d</b>" % (n, num(n * n), n, num(n * n), wz(num(n * n)), n, n, n))
    a, b = R.choice([(9, 16), (36, 64), (25, 144), (81, 144), (16, 9), (64, 36), (9, 40), (144, 256)])
    if math.isqrt(a + b) ** 2 != a + b:
        return None
    s = math.isqrt(a + b)
    return mcq("Berechne %s." % wz("(%d + %d)" % (a, b)), str(s), [str(math.isqrt(a) + math.isqrt(b)), str(s + 1), str(a + b)],
               "Zuerst addieren: %d + %d = %d. %s = <b>%d</b>. Achtung: %s + %s = %d ist falsch." % (a, b, a + b, wz(a + b), s, wz(a), wz(b), math.isqrt(a) + math.isqrt(b)))


def dezbruch():
    kind = R.choice(["dez", "dez", "bruch", "hundert"])
    if kind == "dez":
        n = R.randint(1, 15)
        k = R.choice([1, 2])
        v = Fr(n, 10 ** k)
        sq = v * v
        if n % 10 == 0:
            return None
        return mcq("Berechne %s." % wz(dz(sq)), dz(v), [dz(v * 10) if v * 10 != v else dz(v / 10), dz(v / 10), dz(sq / 2) if (sq / 2 * 10 ** 6).denominator == 1 else dz(v + Fr(1, 10 ** k))],
                   "%s %s %s = %s. Die Wurzel hat halb so viele Nachkommastellen: <b>%s</b>." % (dz(v), MAL, dz(v), dz(sq), dz(v)))
    if kind == "hundert":
        n = R.randint(2, 30)
        e = R.choice([2, 4])
        v = n * 10 ** (e // 2)
        return mcq("Berechne %s." % wz(num(n * n * 10 ** e)), num(v), [num(n * 10 ** e), num(n * 10 ** (e // 2 + 1)), num(n * 10 ** (e // 2 - 1)) if e > 2 else num(v + n)],
                   "%s = %s %s %s = %d %s %s = <b>%s</b>." % (wz(num(n * n * 10 ** e)), wz(num(n * n)), MAL, wz(num(10 ** e)), n, MAL, num(10 ** (e // 2)), num(v)))
    z, nn = R.randint(1, 12), R.randint(2, 13)
    if math.gcd(z, nn) != 1 or z == nn:
        return None
    return mcq("Berechne %s." % wz(bh(Fr(z * z, nn * nn))), bh(Fr(z, nn)), [bh(Fr(z * z, nn)), bh(Fr(z, nn * nn)), bh(Fr(z * z, 2 * nn * nn)) if Fr(z * z, 2 * nn * nn) != Fr(z, nn) else bh(Fr(nn, z))],
               "Wurzel aus Zähler und Nenner: %s %s %s = <b>%s</b>." % (wz(z * z), ":", wz(nn * nn), bh(Fr(z, nn))))


def schaetzen():
    kind = R.choice(["zwischen", "zwischen", "naeher", "runden"])
    n = R.randint(3, 200)
    r = math.isqrt(n)
    if r * r == n:
        return None
    if kind == "zwischen":
        return mcq("Zwischen welchen ganzen Zahlen liegt %s?" % wz(n), "zwischen %d und %d" % (r, r + 1), ["zwischen %d und %d" % (r - 1, r) if r > 1 else "zwischen %d und %d" % (r + 1, r + 2), "zwischen %d und %d" % (n // 2, n // 2 + 1), "zwischen %d und %d" % (r + 1, r + 2)],
                   "%d<sup>2</sup> = %d &lt; %d &lt; %d = %d<sup>2</sup>. Also liegt %s <b>zwischen %d und %d</b>." % (r, r * r, n, (r + 1) ** 2, r + 1, wz(n), r, r + 1))
    if kind == "naeher":
        near = r if n - r * r < (r + 1) ** 2 - n else r + 1
        if n - r * r == (r + 1) ** 2 - n:
            return None
        return mcq("Welcher ganzen Zahl liegt %s am nächsten?" % wz(n), str(near), [str(r if near == r + 1 else r + 1), str(n // 2), str(near + 2) if near + 2 != n // 2 else str(near - 2)],
                   "%d liegt zwischen %d und %d, näher an %d. Also <b>%s ≈ %d</b>." % (n, r * r, (r + 1) ** 2, near * near, wz(n), near))
    v = math.sqrt(n)
    a = Fr(int(v * 10 + 0.5), 10)
    return mcq("Runde %s auf eine Nachkommastelle (Taschenrechner)." % wz(n), dz(a), [dz(Fr(int(v * 10), 10)) if Fr(int(v * 10), 10) != a else dz(a + Fr(1, 10)), dz(a + Fr(2, 10)), dz(Fr(n, 2)) if Fr(n, 2) != a else dz(a - Fr(1, 10))],
               "%s = %s… ≈ <b>%s</b>. Probe: %s<sup>2</sup> = %s." % (wz(n), dz(Fr(int(v * 1000), 1000)), dz(a), dz(a), dz(a * a)))


ZAHLEN = [
    (wz(2), "irrational"), (wz(3), "irrational"), (wz(5), "irrational"), (wz(10), "irrational"), ("π", "irrational"), (wz(50), "irrational"),
    (wz(16), "rational"), (wz(81), "rational"), (wz("0,25"), "rational"), ("0,<span class='ov'>3</span>", "rational"), ("−7", "rational"), (bh(Fr(2, 7)), "rational"),
    ("1,25", "rational"), (wz(bh(Fr(4, 9))), "rational"), ("0,1010010001…", "irrational"), (wz(8), "irrational"),
]


def mengen():
    kind = R.choice(["art", "art", "menge", "begriff"])
    if kind == "art":
        z, a = R.choice(ZAHLEN)
        why = {"rational": "Sie lässt sich als Bruch schreiben (abbrechende oder periodische Dezimalzahl).", "irrational": "Die Dezimalzahl bricht nicht ab und ist nicht periodisch."}[a]
        return mcq("Ist die Zahl %s rational oder irrational?" % z, a, ["irrational" if a == "rational" else "rational", "weder noch", "beides"], "%s <b>%s</b>." % (why, a))
    if kind == "menge":
        z, best = R.choice([("−4", "ℤ (ganze Zahlen)"), ("12", "ℕ (natürliche Zahlen)"), (bh(Fr(3, 4)), "ℚ (rationale Zahlen)"), (wz(7), "ℝ (reelle Zahlen)"),
                            ("−2,5", "ℚ (rationale Zahlen)"), (wz(36), "ℕ (natürliche Zahlen)"), ("π", "ℝ (reelle Zahlen)"), ("−" + wz(9), "ℤ (ganze Zahlen)")])
        return mcq("Welches ist die kleinste Zahlenmenge, zu der %s gehört?" % z, best, [m for m in ["ℕ (natürliche Zahlen)", "ℤ (ganze Zahlen)", "ℚ (rationale Zahlen)", "ℝ (reelle Zahlen)"] if m != best],
                   "ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ. Die kleinste passende Menge: <b>%s</b>." % best)
    q, a, w = R.choice([
        ("Welche Aussage ist richtig?", "Jede rationale Zahl ist eine reelle Zahl.", ["Jede reelle Zahl ist rational.", "Jede Wurzel ist irrational.", "π ist eine rationale Zahl."]),
        ("Welche Zahl ist irrational?", wz(12), [wz(144), wz("1,44"), "1,2"]),
        ("Welche Zahl ist rational?", wz("0,49"), [wz("4,9"), wz(7), "π"]),
        ("Was gilt für die Dezimaldarstellung einer irrationalen Zahl?", "Sie bricht nicht ab und ist nicht periodisch.", ["Sie bricht immer ab.", "Sie ist immer periodisch.", "Sie hat genau zwei Nachkommastellen."]),
        ("Warum ist %s keine reelle Zahl?" % wz("(−9)"), "Keine reelle Zahl ergibt quadriert −9.", ["Weil −3 quadriert −9 ergibt.", "Weil 9 keine Quadratzahl ist.", "Sie ist eine reelle Zahl: −3."]),
        ("Welche Zahl liegt zwischen 3 und 4?", wz(13), [wz(8), wz(17), wz(4)]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def sache():
    kind = R.choice(["seite", "seite", "umfang", "dez", "fallen"])
    if kind == "seite":
        wo, u, lo, hi = R.choice([("Ein quadratisches Beet", "m", 2, 9), ("Ein quadratischer Tisch", "cm", 60, 120), ("Ein quadratischer Spielplatz", "m", 10, 30),
                                  ("Eine quadratische Fliese", "cm", 10, 40), ("Ein quadratisches Grundstück", "m", 15, 40), ("Ein quadratisches Fenster", "cm", 40, 90)])
        n = R.randint(lo, hi)
        return mcq("%s hat einen Flächeninhalt von %s %s². Wie lang ist eine Seite?" % (wo, num(n * n), u), "%d %s" % (n, u), ["%s %s" % (dz(Fr(n * n, 4)), u), "%s %s" % (dz(Fr(n * n, 2)), u), "%d %s" % (n + 1, u)],
                   "a = %s = <b>%d %s</b>. Nicht halbieren und nicht durch 4 teilen." % (wz(num(n * n)), n, u))
    if kind == "umfang":
        n = R.randint(4, 25)
        return mcq("Ein Quadrat hat den Flächeninhalt %s m². Wie groß ist sein Umfang?" % num(n * n), "%d m" % (4 * n), ["%d m" % n, "%s m" % dz(Fr(n * n, 4)), "%d m" % (2 * n)],
                   "Seite: %s = %d m. Umfang: 4 %s %d m = <b>%d m</b>." % (wz(num(n * n)), n, MAL, n, 4 * n))
    if kind == "dez":
        n = R.choice([2, 3, 5, 6, 7, 8, 10, 12, 15, 20, 50])
        v = math.sqrt(n)
        a = Fr(int(v * 100 + 0.5), 100)
        return mcq("Ein Quadrat hat den Flächeninhalt %d cm². Wie lang ist eine Seite (auf zwei Nachkommastellen gerundet)?" % n, "%s cm" % dz(a), ["%s cm" % dz(Fr(n, 4)), "%s cm" % dz(Fr(n, 2)) if Fr(n, 2) != a else "%s cm" % dz(a + 1), "%s cm" % dz(a + Fr(1, 10))],
                   "a = %s ≈ <b>%s cm</b>." % (wz(n), dz(a)))
    t = R.choice([1, 2, 3, 4])
    h = 5 * t * t
    return mcq("Für einen fallenden Stein gilt ungefähr t = %s (h in m, t in s). Wie lange fällt ein Stein aus %d m Höhe?" % (wz("(h : 5)"), h), "%d s" % t, ["%d s" % (h // 5), "%s s" % dz(Fr(h, 10)) if Fr(h, 10) != t else "%d s" % (t + 1), "%d s" % (t * t + 1) if t * t + 1 != h // 5 else "%d s" % (t + 2)],
               "h : 5 = %d. %s = <b>%d s</b>." % (h // 5, wz(h // 5), t))


def main():
    seen = set()
    sets = [
        ("Quadratwurzeln berechnen", mix(R, seen, [(ganz, 20)])),
        ("Wurzeln aus Dezimalzahlen und Brüchen", mix(R, seen, [(dezbruch, 20)])),
        ("Wurzeln abschätzen", mix(R, seen, [(schaetzen, 20)])),
        ("Rationale und irrationale Zahlen", mix(R, seen, [(mengen, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Die <b>Quadratwurzel</b> %s ist die nicht negative Zahl, die quadriert a ergibt: %s = 7, denn 7<sup>2</sup> = 49." % (wz("a"), wz(49)),
         "Aus negativen Zahlen kann man keine Quadratwurzel ziehen. Die Gleichung x<sup>2</sup> = 49 hat aber zwei Lösungen: 7 und −7.",
         "Wurzeln abschätzen: Suche die benachbarten Quadratzahlen. 30 liegt zwischen 25 und 36, also %s zwischen 5 und 6." % wz(30),
         "<b>Irrationale Zahlen</b> wie %s oder π haben unendlich viele Nachkommastellen ohne Periode. Rationale und irrationale Zahlen bilden zusammen die <b>reellen Zahlen</b> ℝ." % wz(2)],
        [example(wz("0,36"), ["0,6 %s 0,6 = 0,36" % MAL], "0,6"),
         example(wz(bh(Fr(9, 25))), ["%s : %s" % (wz(9), wz(25))], bh(Fr(3, 5))),
         example("%s ≈ ?" % wz(50), ["49 &lt; 50 &lt; 64", "näher an 49"], "etwa 7,1")],
        [["%s = 24,5" % wz(49), "Nicht halbieren: %s = 7" % wz(49)],
         ["%s = 0,3" % wz("0,9"), "0,3<sup>2</sup> = 0,09. %s ≈ 0,95" % wz("0,9")],
         ["%s = %s + %s = 7" % (wz("(9 + 16)"), wz(9), wz(16)), "Erst addieren: %s = 5" % wz(25)]])
    faq = [
        {"q": "Was ist eine Quadratwurzel?", "a": "Die Quadratwurzel aus a ist die nicht negative Zahl, deren Quadrat a ist. √64 = 8, weil 8² = 64."},
        {"q": "Warum gibt es keine Wurzel aus einer negativen Zahl?", "a": "Jede reelle Zahl ergibt quadriert eine Zahl größer oder gleich 0. Darum ist √(−4) keine reelle Zahl."},
        {"q": "Was sind irrationale Zahlen?", "a": "Zahlen, die man nicht als Bruch schreiben kann, z. B. √2 und π. Ihre Dezimaldarstellung bricht nicht ab und ist nicht periodisch."},
        {"q": "Wie schätze ich eine Wurzel ab?", "a": "Suche die nächsten Quadratzahlen darunter und darüber. √20 liegt zwischen √16 = 4 und √25 = 5."},
    ]
    make_unit(R, "quadratwurzeln-und-reelle-zahlen", "Z",
              "Die Schülerinnen und Schüler bestimmen Quadrat- und Kubikwurzeln, schätzen Wurzeln ab, unterscheiden rationale und irrationale Zahlen und ordnen Zahlen den Zahlenmengen ℕ, ℤ, ℚ und ℝ zu (Zusammenfassung).",
              "Quadratwurzeln und reelle Zahlen",
              "Quadratwurzeln und irrationale Zahlen Klasse 8 – Arbeitsblätter mit Lösungen",
              "Quadratwurzeln",
              "Quadratwurzeln für Klasse 8: Wurzeln berechnen und abschätzen, Wurzeln aus Dezimalzahlen und Brüchen, rationale und irrationale Zahlen. 100 Aufgaben mit Lösungen, kostenlos.",
              "√49 = 7, denn 7² = 49.",
              "√2 und π sind irrational. Zusammen mit ℚ bilden sie ℝ.",
              body, faq, sets, 2, grade="klasse-8")


if __name__ == "__main__":
    main()
