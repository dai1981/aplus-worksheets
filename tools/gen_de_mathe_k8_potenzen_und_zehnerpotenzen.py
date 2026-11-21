# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Potenzen und Zehnerpotenzen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k8_potenzen_und_zehnerpotenzen.py
Potenzen berechnen (auch negative Basis), Zehnerpotenzen mit positiven und negativen Exponenten, wissenschaftliche Schreibweise
großer und kleiner Zahlen, Multiplizieren und Dividieren in wissenschaftlicher Schreibweise, Sachaufgaben.
Fehler: 2³ = 6 (Basis mal Exponent), (−3)² und −3² verwechselt, Kommaverschiebung in die falsche Richtung, 10⁻³ als negative Zahl gelesen.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import dz
from de_k8 import mcq

R = random.Random(49801)
G = ":"


def sup(n):
    return "<sup>%s</sup>" % (("−%d" % -n) if n < 0 else str(n))


def p10(n):
    return "10" + sup(n)


def wiss(m, e):
    return "%s %s %s" % (dz(m), MAL, p10(e))


def potenz():
    kind = R.choice(["pos", "neg", "negohne", "bruch", "null"])
    if kind == "pos":
        b, n = R.choice([(2, 3), (2, 5), (3, 3), (3, 4), (4, 3), (5, 3), (2, 6), (6, 2), (7, 2), (2, 7), (10, 4), (11, 2), (12, 2), (15, 2), (9, 3), (5, 4)])
        return mcq("Berechne %d%s." % (b, sup(n)), num(b ** n), [num(b * n), num(n ** b) if n ** b != b ** n else num(b ** n + b), num(b ** (n - 1))],
                   "%s = <b>%s</b>." % ((" %s " % MAL).join([str(b)] * n), num(b ** n)))
    if kind == "neg":
        b, n = R.choice([(2, 3), (2, 4), (3, 2), (3, 3), (4, 2), (5, 2), (2, 5), (1, 7), (1, 8), (10, 3)])
        v = (-b) ** n
        return mcq("Berechne (−%d)%s." % (b, sup(n)), dz(v), [dz(-v), dz(-b * n), dz(b ** n + 1) if v < 0 else dz(-(b ** n) - 1)],
                   "%s Faktoren (−%d): %s Exponent → Ergebnis %s. <b>%s</b>" % (n, b, "gerader" if n % 2 == 0 else "ungerader", "positiv" if v > 0 else "negativ", dz(v)))
    if kind == "negohne":
        b = R.choice([2, 3, 4, 5, 6])
        return mcq("Berechne −%d%s." % (b, sup(2)), dz(-b * b), [dz(b * b), dz(-2 * b), dz(2 * b)],
                   "Die Potenz gilt nur für %d: −(%d %s %d) = <b>%s</b>. Anders als (−%d)%s = %d." % (b, b, MAL, b, dz(-b * b), b, sup(2), b * b))
    if kind == "bruch":
        z, nn = R.choice([(1, 2), (2, 3), (1, 3), (3, 4), (1, 10), (2, 5)])
        e = R.choice([2, 3])
        from de_k6 import bh
        v = Fr(z, nn) ** e
        return mcq("Berechne (%s)%s." % (bh(Fr(z, nn)), sup(e)), bh(v), [bh(Fr(z ** e, nn)), bh(Fr(z * e, nn * e)) if Fr(z * e, nn * e) != v else bh(Fr(z, nn ** e)), bh(Fr(z, nn * e))],
                   "Zähler und Nenner hoch %d: <b>%s</b>." % (e, bh(v)))
    b = R.choice([2, 5, 7, 13, 100])
    return mcq("Berechne %d%s." % (b, sup(0)), "1", ["0", str(b), "nicht definiert"], "Jede Zahl (außer 0) hoch 0 ergibt <b>1</b>.")


def zehner():
    n = R.randint(-6, 9)
    kind = R.choice(["wert", "exp"])
    if n == 0 or n == 1:
        return None
    val = Fr(10) ** n
    if kind == "wert":
        w = [dz(Fr(10) ** -n), dz(Fr(10 * n)) if n > 0 else dz(Fr(-10 * -n)), dz(Fr(10) ** (n + 1)) if n > 0 else dz(Fr(10) ** (n - 1))]
        return mcq("Schreibe %s als Zahl." % p10(n), dz(val), w,
                   ("Eine 1 mit %d Nullen: <b>%s</b>." % (n, dz(val))) if n > 0 else ("%s = 1 %s %s. Die 1 steht an der %d. Stelle nach dem Komma: <b>%s</b>." % (p10(n), G, num(10 ** -n), -n, dz(val))))
    return mcq("Schreibe %s als Zehnerpotenz." % dz(val), p10(n), [p10(-n), p10(n + 1) if n > 0 else p10(n - 1), p10(n - 1) if n > 0 else p10(n + 1)],
               ("%d Nullen nach der 1: <b>%s</b>." % (n, p10(n))) if n > 0 else ("Die 1 steht an der %d. Nachkommastelle: <b>%s</b>." % (-n, p10(n))))


def gross():
    m = Fr(R.randint(11, 99), 10) if R.random() < 0.7 else Fr(R.randint(101, 999), 100)
    e = R.randint(3, 9)
    v = m * 10 ** e
    if v.denominator != 1:
        return None
    kind = R.choice(["hin", "zurueck"])
    if kind == "hin":
        return mcq("Schreibe %s in wissenschaftlicher Schreibweise." % num(int(v)), wiss(m, e), [wiss(m * 10, e - 1), wiss(m, e + 1), wiss(m, e - 1)],
                   "Komma hinter die erste Ziffer: %s. Das Komma wandert %d Stellen: <b>%s</b>." % (dz(m), e, wiss(m, e)))
    return mcq("Schreibe %s als Zahl ohne Zehnerpotenz." % wiss(m, e), num(int(v)), [num(int(v * 10)), num(int(v / 10)) if (v / 10).denominator == 1 else num(int(v * 100)), dz(m * 10 ** (e - 1)) if (m * 10 ** (e - 1)).denominator == 1 and m * 10 ** (e - 1) != v / 10 else num(int(v * 100))],
               "Komma um %d Stellen nach rechts: <b>%s</b>." % (e, num(int(v))))


def klein():
    m = Fr(R.randint(11, 99), 10)
    e = -R.randint(2, 7)
    v = m * Fr(10) ** e
    kind = R.choice(["hin", "zurueck"])
    if kind == "hin":
        return mcq("Schreibe %s in wissenschaftlicher Schreibweise." % dz(v), wiss(m, e), [wiss(m, -e), wiss(m, e + 1), wiss(m, e - 1)],
                   "Komma hinter die erste Ziffer, die nicht 0 ist: %s. Das Komma wandert %d Stellen nach rechts, also Exponent %s: <b>%s</b>." % (dz(m), -e, dz(e), wiss(m, e)))
    return mcq("Schreibe %s als Dezimalzahl." % wiss(m, e), dz(v), [dz(v * 10), dz(v / 10), dz(m * 10 ** -e)],
               "Komma um %d Stellen nach links: <b>%s</b>." % (-e, dz(v)))


def rechnen():
    a, b = R.randint(11, 49), R.randint(11, 49)
    ma, mb = Fr(a, 10), Fr(b, 10)
    ea, eb = R.choice([v for v in range(-5, 9) if v]), R.choice([v for v in range(-5, 9) if v])
    kind = R.choice(["mal", "geteilt", "vergleich"])
    if kind == "mal":
        p = ma * mb
        e = ea + eb
        if p >= 10:
            p, e = p / 10, e + 1
        if (p * 1000).denominator != 1:
            return None
        return mcq("Berechne (%s) %s (%s). Gib das Ergebnis in wissenschaftlicher Schreibweise an." % (wiss(ma, ea), MAL, wiss(mb, eb)), wiss(p, e),
                   [wiss(p, ea * eb) if ea * eb != e else wiss(p, e + 2), wiss(ma + mb, e) if ma + mb < 10 else wiss(p, e - 1), wiss(p * 10, e - 1) if p * 10 < 100 else wiss(p, e + 1)],
                   "Zahlen multiplizieren: %s %s %s = %s. Exponenten addieren: %s + %s = %s. <b>%s</b>" % (dz(ma), MAL, dz(mb), dz(ma * mb), dz(ea), "(%s)" % dz(eb) if eb < 0 else dz(eb), dz(ea + eb), wiss(p, e)))
    if kind == "geteilt":
        q = Fr(R.randint(2, 9))
        mb = Fr(R.randint(11, 30), 10)
        ma = q * mb
        if ma >= 10:
            return None
        e = ea - eb
        return mcq("Berechne (%s) %s (%s)." % (wiss(ma, ea), G, wiss(mb, eb)), wiss(q, e), [wiss(q, ea + eb) if ea + eb != e else wiss(q, e + 1), wiss(q, Fr(ea, eb)) if eb and Fr(ea, eb).denominator == 1 and Fr(ea, eb) != e else wiss(q, e - 1), wiss(ma - mb, e) if ma > mb and ma - mb != q else wiss(q * 10, e - 1)],
                   "%s %s %s = %s, Exponenten subtrahieren: %s − %s = %s. <b>%s</b>" % (dz(ma), G, dz(mb), dz(q), dz(ea), "(%s)" % dz(eb) if eb < 0 else dz(eb), dz(e), wiss(q, e)))
    if ea == eb:
        return None
    va, vb = ma * Fr(10) ** ea, mb * Fr(10) ** eb
    big = wiss(ma, ea) if va > vb else wiss(mb, eb)
    return mcq("Welche Zahl ist größer: %s oder %s?" % (wiss(ma, ea), wiss(mb, eb)), big, [wiss(mb, eb) if va > vb else wiss(ma, ea), "Beide sind gleich groß.", "Das kann man nicht vergleichen."],
               "Zuerst die Exponenten vergleichen: %s ist größer als %s. <b>%s</b>" % (dz(max(ea, eb)), dz(min(ea, eb)), big))


SACH = [
    ("Die Erde ist etwa 150 000 000 km von der Sonne entfernt.", Fr(15, 10), 8, "km"),
    ("Ein menschliches Haar ist etwa 0,08 mm dick.", Fr(8), -2, "mm"),
    ("In Deutschland leben etwa 84 000 000 Menschen.", Fr(84, 10), 7, ""),
    ("Ein Bakterium ist etwa 0,002 mm lang.", Fr(2), -3, "mm"),
    ("Licht legt in einer Sekunde etwa 300 000 km zurück.", Fr(3), 5, "km"),
    ("Ein Sandkorn wiegt etwa 0,0006 g.", Fr(6), -4, "g"),
    ("Der Mond ist etwa 384 000 km von der Erde entfernt.", Fr(384, 100), 5, "km"),
    ("Ein Wassertropfen hat ein Volumen von etwa 0,05 ml.", Fr(5), -2, "ml"),
    ("Die Erde hat etwa 8 100 000 000 Einwohner.", Fr(81, 10), 9, ""),
    ("Ein Virus ist etwa 0,0001 mm groß.", Fr(1), -4, "mm"),
    ("Der Bodensee enthält etwa 48 000 000 000 m³ Wasser.", Fr(48, 10), 10, "m³"),
    ("Eine Ameise wiegt etwa 0,003 g.", Fr(3), -3, "g"),
    ("Der Durchmesser der Sonne beträgt etwa 1 400 000 km.", Fr(14, 10), 6, "km"),
    ("Ein Blatt Papier ist etwa 0,1 mm dick.", Fr(1), -1, "mm"),
    ("Ein Elefant wiegt etwa 6 000 kg.", Fr(6), 3, "kg"),
    ("Ein rotes Blutkörperchen ist etwa 0,007 mm groß.", Fr(7), -3, "mm"),
]


def sache():
    t, m, e, u = R.choice(SACH)
    kind = R.choice(["schreib", "schreib", "faktor"])
    if kind == "schreib":
        return mcq(t + " Wie lautet die Zahl in wissenschaftlicher Schreibweise?", wiss(m, e) + (" " + u if u else ""), [wiss(m, -e) + (" " + u if u else ""), wiss(m, e + 1) + (" " + u if u else ""), wiss(m * 10, e) + (" " + u if u else "")],
                   "Komma hinter die erste gültige Ziffer, Stellen zählen: <b>%s</b>." % (wiss(m, e) + (" " + u if u else "")))
    k = R.choice([10, 100, 1000])
    import math
    d = int(round(math.log10(k)))
    return mcq(t + " Wie groß ist das %s-Fache davon in wissenschaftlicher Schreibweise?" % num(k), wiss(m, e + d) + (" " + u if u else ""), [wiss(m, e * d) + (" " + u if u else "") if e * d != e + d else wiss(m, e + d + 1) + (" " + u if u else ""), wiss(m * k, e) + (" " + u if u else ""), wiss(m, e - d) + (" " + u if u else "")],
               "Mal %s = mal %s: Exponent %s + %d = %s. <b>%s</b>" % (num(k), p10(d), dz(e), d, dz(e + d), wiss(m, e + d) + (" " + u if u else "")))


def main():
    seen = set()
    sets = [
        ("Potenzen berechnen", mix(R, seen, [(potenz, 20)])),
        ("Zehnerpotenzen", mix(R, seen, [(zehner, 20)])),
        ("Große und kleine Zahlen", mix(R, seen, [(gross, 10), (klein, 10)])),
        ("Rechnen mit Zehnerpotenzen", mix(R, seen, [(rechnen, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Eine <b>Potenz</b> a<sup>n</sup> ist ein Produkt aus n gleichen Faktoren a. Beispiel: 2<sup>3</sup> = 2 %s 2 %s 2 = 8." % (MAL, MAL),
         "Bei negativer Basis braucht man Klammern: (−3)<sup>2</sup> = 9, aber −3<sup>2</sup> = −9.",
         "<b>Zehnerpotenzen</b>: 10<sup>4</sup> = 10 000, 10<sup>0</sup> = 1, 10<sup>−3</sup> = 0,001.",
         "<b>Wissenschaftliche Schreibweise</b>: Zahl zwischen 1 und 10 mal Zehnerpotenz, z. B. 3,8 %s 10<sup>5</sup>. Große Zahlen haben einen positiven, kleine Zahlen einen negativen Exponenten." % MAL],
        [example("45 000 000", ["Komma hinter die 4: 4,5", "7 Stellen"], "4,5 %s 10<sup>7</sup>" % MAL),
         example("0,00032", ["Komma hinter die 3: 3,2", "4 Stellen nach rechts"], "3,2 %s 10<sup>−4</sup>" % MAL),
         example("(2 %s 10<sup>3</sup>) %s (4 %s 10<sup>5</sup>)" % (MAL, MAL, MAL), ["2 %s 4 = 8, 3 + 5 = 8" % MAL], "8 %s 10<sup>8</sup>" % MAL)],
        [["2<sup>3</sup> = 6", "2<sup>3</sup> = 2 %s 2 %s 2 = 8" % (MAL, MAL)],
         ["10<sup>−3</sup> ist eine negative Zahl", "10<sup>−3</sup> = 0,001 ist positiv und klein"],
         ["45 000 = 45 %s 10<sup>3</sup> ist wissenschaftlich" % MAL, "Die Zahl vorne liegt zwischen 1 und 10: 4,5 %s 10<sup>4</sup>" % MAL]])
    faq = [
        {"q": "Was ist die wissenschaftliche Schreibweise?", "a": "Man schreibt eine Zahl als Produkt aus einer Zahl zwischen 1 und 10 und einer Zehnerpotenz, z. B. 2,5 · 10^6."},
        {"q": "Was bedeutet ein negativer Exponent bei 10?", "a": "10^−n = 1 : 10^n. Zum Beispiel ist 10^−2 = 0,01. Die Zahl ist klein, aber positiv."},
        {"q": "Warum ist (−2)^4 positiv?", "a": "Vier negative Faktoren ergeben ein positives Produkt. Bei ungeradem Exponenten ist das Ergebnis negativ."},
        {"q": "Wie multipliziert man Zahlen in wissenschaftlicher Schreibweise?", "a": "Die Zahlen vorne multiplizieren und die Exponenten addieren. Liegt das Ergebnis vorne über 10, wird es angepasst."},
    ]
    make_unit(R, "potenzen-und-zehnerpotenzen", "Z",
              "Die Schülerinnen und Schüler berechnen Potenzen mit natürlichen Exponenten, nutzen Zehnerpotenzen mit positiven und negativen Exponenten und stellen sehr große und sehr kleine Zahlen in wissenschaftlicher Schreibweise dar (Zusammenfassung).",
              "Potenzen und Zehnerpotenzen",
              "Potenzen und Zehnerpotenzen Klasse 8 – wissenschaftliche Schreibweise, Arbeitsblätter",
              "Zehnerpotenzen",
              "Potenzen für Klasse 8: Potenzen berechnen, Zehnerpotenzen, große und kleine Zahlen in wissenschaftlicher Schreibweise und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Wissenschaftliche Schreibweise: 3,8 · 10⁵",
              "Große Zahlen: positiver Exponent. Kleine Zahlen: negativer Exponent.",
              body, faq, sets, 1, grade="klasse-8")


if __name__ == "__main__":
    main()
