# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Dezimalzahlen addieren und subtrahieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_dezimalzahlen_addieren_und_subtrahieren.py
Kopfrechnen mit Zehnteln und Hundertsteln, schriftlich addieren und subtrahieren (Komma unter Komma), Ergänzen, Überschlag, Sachaufgaben mit Geld und Größen.
Fehler: Stellen rechtsbündig statt Komma unter Komma, Übertrag über das Komma vergessen, 1 − 0,35 = 0,75.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz, mcq

R = random.Random(49609)
KIDS = Kids(R)


def zahl(maxg, k):
    n = R.randint(1, 10 ** k - 1)
    if n % 10 == 0 and k > 1:
        n += 1
    return Fr(R.randint(0, maxg)) + Fr(n, 10 ** k)


def stellen(v):
    s = dz(v)
    return len(s.split(",")[1]) if "," in s else 0


def rechts(a, b, op):
    """Fehler: Ziffern rechtsbündig ohne Komma"""
    sa, sb = dz(a).replace(",", ""), dz(b).replace(",", "")
    ka, kb = stellen(a), stellen(b)
    k = max(ka, kb)
    ia, ib = int(sa), int(sb)
    r = ia + ib if op == "+" else ia - ib
    if r <= 0:
        return None
    return dz(Fr(r, 10 ** k))


def kopf():
    k = R.choice([1, 1, 2])
    a, b = zahl(9, k), zahl(9, k)
    op = R.choice(["+", "−"])
    if op == "−" and a < b:
        a, b = b, a
    if a == b:
        return None
    v = a + b if op == "+" else a - b
    f = Fr(1, 10 ** k)
    return mcq("%s %s %s = ?" % (dz(a), op, dz(b)), dz(v), [dz(v + f) if v + f > 0 else None, dz(v - f) if v - f > 0 else None, dz(v + 1), dz(v * 10) if (v * 10) != v else None],
               "%s %s %s = <b>%s</b>." % (dz(a), op, dz(b), dz(v)))


def schriftlich():
    ka, kb = R.sample([1, 2, 3], 2)
    a, b = zahl(99, ka), zahl(99, kb)
    op = R.choice(["+", "+", "−", "−"])
    if op == "−" and a < b:
        a, b = b, a
    if a == b:
        return None
    v = a + b if op == "+" else a - b
    k = max(ka, kb)
    return mcq("Rechne schriftlich: %s %s %s" % (dz(a), op, dz(b)), dz(v), [rechts(a, b, op), dz(v + Fr(1, 10 ** min(ka, kb))) if v + Fr(1, 10 ** min(ka, kb)) != v else None, dz(v + 1) if op == "+" else dz(v - 1) if v > 1 else dz(v + 1), dz(v + Fr(1, 10))],
               "Komma unter Komma schreiben und mit Nullen auffüllen: %s %s %s = <b>%s</b>." % (dz(a), op, dz(b), dz(v)))


def ergaenzen():
    kind = R.choice(["eins", "zehn", "luecke"])
    if kind == "eins":
        x = zahl(0, R.choice([1, 2]))
        x100 = int(x * 100)
        typ = Fr((10 - x100 // 10) % 10, 10) + Fr((10 - x100 % 10) % 10, 100)
        return mcq("Ergänze zu 1: %s + ☐ = 1" % dz(x), dz(1 - x), [dz(typ) if typ != 1 - x and typ > 0 else None, dz(1 - x + Fr(1, 10)) if 1 - x + Fr(1, 10) < 1 else None, dz(1 - x - Fr(1, 100)) if stellen(x) == 2 else dz(1 - x + Fr(1, 100)), dz(1 - x + Fr(1, 100))],
                   "1 − %s = <b>%s</b>. Probe: %s + %s = 1." % (dz(x), dz(1 - x), dz(x), dz(1 - x)))
    if kind == "zehn":
        x = zahl(9, 2)
        return mcq("Ergänze zu 10: %s + ☐ = 10" % dz(x), dz(10 - x), [dz(10 - x + Fr(1, 10)), dz(9 - x) if x < 9 else dz(11 - x), dz(10 - x - Fr(1, 100))],
                   "10 − %s = <b>%s</b>." % (dz(x), dz(10 - x)))
    a, b = zahl(20, 2), zahl(20, 1)
    s = a + b
    return mcq("Welche Zahl fehlt? %s + ☐ = %s" % (dz(a), dz(s)), dz(b), [dz(s + a), dz(b + Fr(1, 10)), dz(b - Fr(1, 100)) if b > Fr(1, 100) else None, rechts(s, a, "−")],
               "Umkehraufgabe: %s − %s = <b>%s</b>." % (dz(s), dz(a), dz(b)))


def ueberschlag():
    a, b, c = zahl(50, 2), zahl(50, 2), zahl(30, 1)
    v = a + b - c
    if v <= 0:
        return None
    rd = lambda x: int(x + Fr(1, 2))
    r = rd(a) + rd(b) - rd(c)
    return mcq("Überschlage: %s + %s − %s ≈ ?" % (dz(a), dz(b), dz(c)), "≈ %d" % r, ["≈ %d" % x for x in (r + 10, r - 10 if r > 10 else r + 20, rd(a) + rd(b) + rd(c))],
               "Auf Ganze runden: %d + %d − %d = <b>%d</b>. (Genau: %s)" % (rd(a), rd(b), rd(c), r, dz(v)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["einkauf", "rest", "sprung", "zeit", "laenge", "kasse"])
    if kind == "einkauf":
        items = R.sample([("ein Heft", 1.2, 2.9), ("einen Stift", 0.8, 2.5), ("ein Buch", 7.9, 16.9), ("eine Brezel", 0.6, 1.4), ("einen Saft", 0.9, 2.2), ("einen Radiergummi", 0.4, 1.1)], 3)
        vals = [Fr(int(R.uniform(lo, hi) * 100) // 5 * 5, 100) for _, lo, hi in items]
        t = sum(vals)
        return mcq("%s kauft %s für %s €, %s für %s € und %s für %s €. Wie viel muss %s bezahlen?" % (p, items[0][0], dz(vals[0]), items[1][0], dz(vals[1]), items[2][0], dz(vals[2]), er),
                   "%s €" % ("%d,%02d" % (int(t), int((t * 100) % 100))), ["%d,%02d €" % (int(x), int((x * 100) % 100)) for x in (t + Fr(1, 10), t - Fr(1, 10), t + 1)],
                   "%s + %s + %s = <b>%d,%02d €</b>." % (dz(vals[0]), dz(vals[1]), dz(vals[2]), int(t), int((t * 100) % 100)))
    if kind in ("rest", "kasse"):
        b = R.choice([10, 20, 50])
        c = Fr(R.randint(150, b * 100 - 50), 100)
        r = b - c
        f = lambda x: "%d,%02d €" % (int(x), int((x * 100) % 100))
        return mcq("%s bezahlt einen Einkauf von %s € mit einem %d-€-Schein. Wie viel Rückgeld bekommt %s?" % (p, f(c).replace(" €", ""), b, er), f(r), [f(r + Fr(1, 10)), f(r - Fr(1, 100)) if r > Fr(1, 100) else f(r + 1), f(r + 1)],
                   "%d − %s = <b>%s</b>." % (b, f(c).replace(" €", ""), f(r)))
    if kind == "sprung":
        a, b = Fr(R.randint(250, 420), 100), Fr(R.randint(250, 420), 100)
        if a == b:
            return None
        hi, lo = max(a, b), min(a, b)
        p2, _ = KIDS.next()
        return mcq("Beim Weitsprung springt %s %s m und %s %s m. Wie groß ist der Unterschied?" % (p, dz(a), p2, dz(b)), "%s m" % dz(hi - lo), ["%s m" % dz(x) for x in (hi + lo, hi - lo + Fr(1, 10), (hi - lo) * 10)],
                   "%s − %s = <b>%s m</b>." % (dz(hi), dz(lo), dz(hi - lo)))
    if kind == "zeit":
        a, b = Fr(R.randint(1150, 1499), 100), Fr(R.randint(1150, 1499), 100)
        if a == b:
            return None
        hi, lo = max(a, b), min(a, b)
        p2, _ = KIDS.next()
        return mcq("Beim 100-m-Lauf braucht %s %s s und %s %s s. Um wie viele Sekunden war der Schnellere schneller?" % (p, dz(a), p2, dz(b)), "%s s" % dz(hi - lo), ["%s s" % dz(x) for x in (hi - lo + Fr(1, 10), (hi - lo) * 10, hi - lo + 1)],
                   "%s − %s = <b>%s s</b>." % (dz(hi), dz(lo), dz(hi - lo)))
    a, b, c = Fr(R.randint(105, 480), 100), Fr(R.randint(35, 95), 100), Fr(R.randint(5, 9), 10)
    v = a - b - c
    if v <= 0:
        return None
    return mcq("Von einem %s m langen Seil schneidet %s erst %s m und dann %s m ab. Wie lang ist der Rest?" % (dz(a), p, dz(b), dz(c)), "%s m" % dz(v), ["%s m" % dz(x) for x in (a - b + c, v + Fr(1, 10), v + Fr(1, 100))],
               "%s − %s − %s = <b>%s m</b>." % (dz(a), dz(b), dz(c), dz(v)))


def main():
    seen = set()
    sets = [
        ("Kopfrechnen", mix(R, seen, [(kopf, 20)])),
        ("Schriftlich rechnen", mix(R, seen, [(schriftlich, 20)])),
        ("Ergänzen", mix(R, seen, [(ergaenzen, 20)])),
        ("Überschlagen und rechnen", mix(R, seen, [(ueberschlag, 8), (schriftlich, 12)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Beim Addieren und Subtrahieren von Dezimalzahlen schreibt man <b>Komma unter Komma</b>.",
         "Fehlende Stellen füllt man mit <b>Nullen</b> auf: 4,5 − 1,27 wird 4,50 − 1,27.",
         "Dann rechnet man wie mit natürlichen Zahlen und setzt das Komma im Ergebnis an dieselbe Stelle.",
         "Ein <b>Überschlag</b> mit gerundeten Zahlen zeigt, ob das Ergebnis stimmen kann."],
        [example("12,7 + 3,48", ["12,70 + 3,48", "Komma unter Komma"], "16,18"),
         example("5 − 2,35", ["5,00 − 2,35"], "2,65")],
        [["12,7 + 3,48 = 4,75 (rechtsbündig)", "Komma unter Komma: 16,18"],
         ["1 − 0,35 = 0,75", "1,00 − 0,35 = 0,65"],
         ["0,8 + 0,5 = 0,13", "8 Zehntel + 5 Zehntel = 13 Zehntel = 1,3"]])
    faq = [
        {"q": "Wie addiert man Dezimalzahlen schriftlich?", "a": "Komma unter Komma schreiben, mit Nullen auffüllen und wie gewohnt addieren. Das Komma kommt im Ergebnis an dieselbe Stelle."},
        {"q": "Warum füllt man mit Nullen auf?", "a": "Damit beide Zahlen gleich viele Stellen nach dem Komma haben. 4,5 = 4,50 – der Wert ändert sich nicht."},
        {"q": "Wie prüfe ich mein Ergebnis?", "a": "Mit einem Überschlag (auf Ganze runden) oder mit der Umkehraufgabe."},
        {"q": "Was ist 0,7 + 0,6?", "a": "7 Zehntel + 6 Zehntel = 13 Zehntel = 1,3."},
    ]
    make_unit(R, "dezimalzahlen-addieren-und-subtrahieren", "Z",
              "Die Schülerinnen und Schüler addieren und subtrahieren Dezimalzahlen im Kopf und schriftlich, überschlagen Ergebnisse und lösen Sachaufgaben mit Geld und Größen (Zusammenfassung).",
              "Dezimalzahlen addieren und subtrahieren",
              "Dezimalzahlen addieren und subtrahieren Klasse 6 – Arbeitsblätter",
              "Dezimalzahlen addieren",
              "Dezimalzahlen addieren und subtrahieren für Klasse 6: Kopfrechnen, schriftlich, ergänzen, überschlagen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Komma unter Komma.",
              "Fehlende Stellen mit Nullen auffüllen.",
              body, faq, sets, 9, grade="klasse-6")


if __name__ == "__main__":
    main()
