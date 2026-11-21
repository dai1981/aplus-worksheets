# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Brüche und Dezimalzahlen umwandeln（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_brueche_und_dezimalzahlen.py
Bruch → Dezimalzahl (erweitern auf 10, 100, 1000 oder dividieren), Dezimalzahl → gekürzter Bruch, periodische Dezimalzahlen, Brüche und Dezimalzahlen vergleichen, Sachaufgaben.
Fehler: 3/4 = 3,4 (Zähler, Komma, Nenner), 0,25 = 25/10, Periode übersehen (1/3 = 0,3), nicht gekürzt.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table
from de_k6 import bh, dz, endlich, mcq

R = random.Random(49608)
KIDS = Kids(R)
LT, GT = "&lt;", "&gt;"


def per(v):
    """Dezimalzahl mit Periode: 0,1<ov>6</ov>"""
    v = Fr(v)
    ip, r = divmod(v.numerator, v.denominator)
    d = v.denominator
    digits, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // d))
        r %= d
    if not r:
        return dz(v)
    k = seen[r]
    return "%d,%s<span class='ov'>%s</span>" % (ip, "".join(digits[:k]), "".join(digits[k:]))


EASY = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20), (7, 20), (1, 25), (4, 25), (6, 25), (1, 50), (3, 50), (1, 8), (3, 8), (5, 8), (7, 8)]


def zu_dez():
    z, n = R.choice(EASY)
    w = R.choice([0, 0, 0, 1, 2, 3])
    v = w + Fr(z, n)
    q = ("Schreibe %s als Dezimalzahl." % fr(z, n)) if w == 0 else ("Schreibe %d%s als Dezimalzahl." % (w, " " + fr(z, n)))
    f = 1
    while (n * f) not in (10, 100, 1000):
        f += 1
    return mcq(q, dz(v), ["%d,%d" % (z, n) if w == 0 else "%d,%d%d" % (w, z, n), dz(w + Fr(z * f, n * f * 10)), dz(w + Fr(n, 100)) if n < 100 else dz(w + Fr(z, 10)), dz(v + Fr(1, 10))],
               ("Erweitern auf %d: %s = %s = <b>%s</b>." % (n * f, fr(z, n), fr(z * f, n * f), dz(v))) if f > 1 else "Zehntel: %s = <b>%s</b>." % (fr(z, n), dz(v)))


def zu_bruch():
    k = R.choice([1, 2, 2, 3])
    n = R.randint(1, 10 ** k - 1)
    if n % 10 == 0:
        return None
    v = Fr(n, 10 ** k)
    raw = fr(n, 10 ** k)
    wrong = [fr(n, 10 ** (k - 1)) if k > 1 else fr(n, 100), raw if bh(v) != raw else fr(n, 10 ** (k + 1)), fr(1, n) if n > 1 else fr(1, 100), bh(v + Fr(1, v.denominator))]
    return mcq("Schreibe %s als vollständig gekürzten Bruch." % dz(v), bh(v), wrong,
               "%d Stelle%s nach dem Komma: %s%s." % (k, "n" if k > 1 else "", raw, (" = <b>%s</b>" % bh(v)) if bh(v) != raw else " (lässt sich nicht kürzen)"))


def periodisch():
    kind = R.choice(["welche", "zu", "zu"])
    n = R.choice([3, 6, 7, 9, 11, 12, 15])
    z = R.randint(1, n - 1)
    if gcd(z, n) > 1:
        return None
    v = Fr(z, n)
    if kind == "welche":
        good = fr(z, n)
        bads = [fr(a, b) for a, b in R.sample(EASY, 3)]
        return mcq("Welcher Bruch ergibt eine <b>periodische</b> Dezimalzahl? %s" % ", ".join(sorted(bads + [good])), good, bads,
                   "Der Nenner %d hat einen Primfaktor außer 2 und 5. %s = %s. <b>%s</b>" % (n, fr(z, n), per(v), good))
    p = per(v)
    plain = p.replace("<span class='ov'>", "").replace("</span>", "")
    return mcq("Schreibe %s als Dezimalzahl." % fr(z, n), p, [plain, "%d,%d" % (z, n), per(v + Fr(1, 10)) if per(v + Fr(1, 10)) != p else None, per(Fr(z, n * 10))],
               "%d : %d = %s … Die Ziffern wiederholen sich: <b>%s</b>." % (z, n, plain + plain.split(",")[1][-1], p))


def vergleich():
    z, n = R.choice(EASY + [(1, 3), (2, 3), (1, 6), (5, 6)])
    v = Fr(z, n)
    d = v + Fr(R.choice([-3, -2, -1, 1, 2, 3]), 100)
    if d <= 0 or not endlich(d):
        return None
    s = LT if v < d else GT
    return mcq("Setze &lt;, &gt; oder = ein: %s ☐ %s" % (fr(z, n), dz(d)), s, [t for t in (LT, GT, "=") if t != s] + ["≈"],
               "%s = %s. Also <b>%s %s %s</b>." % (fr(z, n), per(v), fr(z, n), s, dz(d)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["geld", "zeit", "laenge", "test", "liter"])
    if kind == "geld":
        z, n = R.choice([(1, 4), (3, 4), (1, 2), (1, 5), (2, 5), (1, 10), (3, 10), (1, 20)])
        e = R.choice([4, 8, 10, 20, 40, 60, 100])
        v = e * Fr(z, n)
        if not endlich(v):
            return None
        return mcq("%s gibt %s von %d € aus. Wie viel Euro sind das? Schreibe mit Komma." % (p, fr(z, n), e), "%s €" % (dz(v) if v.denominator == 1 else dz(v) + ("0" if len(dz(v).split(",")[1]) == 1 else "")) if v.denominator != 1 else "%s €" % dz(v),
                   ["%d,%d €" % (z, n), "%s €" % dz(v * 10), "%s €" % dz(Fr(e, n))], "%d € %s %s = <b>%s €</b>." % (e, MAL, fr(z, n), dz(v)))
    if kind == "zeit":
        z, n = R.choice([(1, 4), (3, 4), (1, 2), (1, 5), (1, 10), (3, 10)])
        w = R.randint(1, 4)
        v = w + Fr(z, n)
        return mcq("Ein Film dauert %s h. Wie viele Stunden sind das als Dezimalzahl?" % (str(w) + " " + fr(z, n)), "%s h" % dz(v), ["%d,%d h" % (w, z * 60 // n), "%d,%d h" % (w, z), "%s h" % dz(v + Fr(1, 10))],
                   "%s = %s. <b>%s h</b>. (Achtung: %s h sind %d min, nicht %d,%d h.)" % (fr(z, n), dz(Fr(z, n)), dz(v), fr(z, n), z * 60 // n, w, z * 60 // n))
    if kind == "laenge":
        z, n = R.choice([(1, 4), (3, 4), (1, 2), (2, 5), (1, 8), (3, 8), (1, 20)])
        return mcq("%s m sind wie viele Meter als Dezimalzahl?" % fr(z, n), "%s m" % dz(Fr(z, n)), ["%d,%d m" % (z, n), "%s m" % dz(Fr(z, n) / 10), "%s m" % dz(Fr(n, 100))],
                   "%s = %s = <b>%s m</b>." % (fr(z, n), dz(Fr(z, n)), dz(Fr(z, n))))
    if kind == "test":
        t = R.choice([20, 25, 40, 50])
        r = R.randint(t // 2, t - 1)
        v = Fr(r, t)
        return mcq("%s hat %d von %d Punkten. Gib den Anteil als Dezimalzahl an." % (p, r, t), dz(v), ["%d,%d" % (r, t), dz(Fr(t - r, t)), dz(v + Fr(1, 10)) if v + Fr(1, 10) < 1 else dz(v - Fr(1, 10))],
                   "%s = %s = <b>%s</b>." % (fr(r, t), bh(v), dz(v)))
    z, n = R.choice([(1, 4), (3, 4), (1, 2), (1, 5), (3, 5), (1, 8)])
    k = R.randint(2, 6)
    v = k * Fr(z, n)
    if v.denominator == 1:
        return None
    return mcq("%s füllt %d Becher mit je %s l Wasser. Wie viele Liter sind das als Dezimalzahl?" % (p, k, fr(z, n)), "%s l" % dz(v), ["%s l" % dz(k + Fr(z, n * 10)), "%d,%d l" % (k * z, n), "%s l" % dz(v + Fr(1, 2))],
               "%d %s %s = %s = <b>%s l</b>." % (k, MAL, fr(z, n), bh(v, True), dz(v)))


def main():
    seen = set()
    sets = [
        ("Bruch in Dezimalzahl", mix(R, seen, [(zu_dez, 20)])),
        ("Dezimalzahl in Bruch", mix(R, seen, [(zu_bruch, 20)])),
        ("Periodische Dezimalzahlen", mix(R, seen, [(periodisch, 20)])),
        ("Brüche und Dezimalzahlen vergleichen", mix(R, seen, [(vergleich, 14), (zu_dez, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Bruch → Dezimalzahl</b>: Auf den Nenner 10, 100 oder 1000 erweitern. Geht das nicht, den Zähler durch den Nenner dividieren.",
         "<b>Dezimalzahl → Bruch</b>: Die Stellen nach dem Komma geben den Nenner (1 Stelle: 10, 2 Stellen: 100, 3 Stellen: 1000). Dann kürzen.",
         "Hat der gekürzte Nenner einen Primfaktor außer 2 und 5, entsteht eine <b>periodische Dezimalzahl</b>: %s = 0,<span class='ov'>3</span>." % fr(1, 3),
         "Den Strich über der Periode liest man „Periode“: 0,1<span class='ov'>6</span> = 0,1666…"],
        [example("%s als Dezimalzahl" % fr(3, 8), ["%s = %s" % (fr(3, 8), fr(375, 1000))], "0,375"),
         example("0,45 als Bruch", ["%s" % fr(45, 100), "durch 5 kürzen"], fr(9, 20))],
        [["%s = 3,4" % fr(3, 4), "%s = %s = 0,75" % (fr(3, 4), fr(75, 100))],
         ["0,25 = %s" % fr(25, 10), "Zwei Stellen: %s = %s" % (fr(25, 100), fr(1, 4))],
         ["%s = 0,3" % fr(1, 3), "%s = 0,333… = 0,<span class='ov'>3</span>" % fr(1, 3)]],
        extra=table(["Bruch", "Dezimalzahl"], [[fr(1, 2), "0,5"], [fr(1, 4), "0,25"], [fr(3, 4), "0,75"], [fr(1, 5), "0,2"], [fr(1, 8), "0,125"], [fr(1, 3), "0,<span class='ov'>3</span>"]]))
    faq = [
        {"q": "Wie wandelt man einen Bruch in eine Dezimalzahl um?", "a": "Auf 10, 100 oder 1000 erweitern (3/4 = 75/100 = 0,75) oder den Zähler durch den Nenner teilen."},
        {"q": "Wie wandelt man eine Dezimalzahl in einen Bruch um?", "a": "0,35 = 35/100. Danach kürzen: 35/100 = 7/20."},
        {"q": "Was ist eine periodische Dezimalzahl?", "a": "Eine Dezimalzahl, bei der sich Ziffern immer wiederholen, z. B. 1/3 = 0,333… Man schreibt einen Strich über die Periode."},
        {"q": "Welche Brüche ergeben abbrechende Dezimalzahlen?", "a": "Gekürzte Brüche, deren Nenner nur die Primfaktoren 2 und 5 hat, z. B. 1/8 = 0,125."},
    ]
    make_unit(R, "brueche-und-dezimalzahlen", "Z",
              "Die Schülerinnen und Schüler wandeln Brüche und Dezimalzahlen ineinander um, erkennen abbrechende und periodische Dezimalzahlen und vergleichen Brüche mit Dezimalzahlen (Zusammenfassung).",
              "Brüche und Dezimalzahlen umwandeln",
              "Brüche in Dezimalzahlen umwandeln Klasse 6 – Arbeitsblätter",
              "Bruch ↔ Dezimalzahl",
              "Brüche und Dezimalzahlen für Klasse 6: umwandeln, periodische Dezimalzahlen, vergleichen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Auf 10, 100 oder 1000 erweitern – oder Zähler durch Nenner teilen.",
              "Nenner nur mit 2 und 5: abbrechend. Sonst periodisch.",
              body, faq, sets, 8, grade="klasse-6")


if __name__ == "__main__":
    main()
