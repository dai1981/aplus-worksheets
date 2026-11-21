# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Dezimalzahlen multiplizieren und dividieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_dezimalzahlen_multiplizieren_und_dividieren.py
Mal und durch 10, 100, 1000 (Komma verschieben), Dezimalzahl mal natürliche Zahl, Dezimalzahl mal Dezimalzahl (Stellen zählen), Division durch natürliche Zahlen und durch Dezimalzahlen, Sachaufgaben.
Fehler: Komma in die falsche Richtung verschoben, Stellen nach dem Komma falsch gezählt (0,3 · 0,2 = 0,6), beim Teilen durch eine Dezimalzahl das Komma nur bei einer Zahl verschoben.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz, endlich, mcq

R = random.Random(49610)
KIDS = Kids(R)
G = ":"


def st(v):
    s = dz(v)
    return len(s.split(",")[1]) if "," in s else 0


def zehner():
    k = R.choice([1, 2, 3])
    f = 10 ** k
    v = Fr(R.randint(1, 9999), 10 ** R.randint(1, 3))
    op = R.choice(["mal", "durch"])
    if op == "mal":
        r = v * f
        return mcq("%s %s %d = ?" % (dz(v), MAL, f), dz(r), [dz(v / f), dz(v * f * 10), dz(v * f / 10) if f > 10 else dz(v * 1000)],
                   "Mal %d: Das Komma rückt um %d Stelle%s nach <b>rechts</b>. <b>%s</b>" % (f, k, "n" if k > 1 else "", dz(r)))
    r = v / f
    return mcq("%s %s %d = ?" % (dz(v), G, f), dz(r), [dz(v * f), dz(v / f / 10), dz(v / f * 10) if f > 10 else dz(v / 1000)],
               "Durch %d: Das Komma rückt um %d Stelle%s nach <b>links</b>. <b>%s</b>" % (f, k, "n" if k > 1 else "", dz(r)))


def mal_zahl():
    v = Fr(R.randint(11, 999), 10 ** R.randint(1, 2))
    if v.denominator == 1:
        return None
    k = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 11, 12])
    r = v * k
    return mcq("%s %s %d = ?" % (dz(v), MAL, k), dz(r), [dz(r * 10), dz(r / 10), dz(r + Fr(1, 10)), dz(r + k * Fr(1, 10 ** st(v)))],
               "Ohne Komma rechnen: %s %s %d = %s. %d Stelle%s nach dem Komma: <b>%s</b>." % (dz(v).replace(",", "").lstrip("0") or "0", MAL, k, dz(r * 10 ** st(v)), st(v), "n" if st(v) > 1 else "", dz(r)))


def mal_dez():
    a = Fr(R.randint(1, 99), 10 ** R.randint(1, 2))
    b = Fr(R.randint(1, 99), 10 ** R.randint(1, 2))
    if a.denominator == 1 or b.denominator == 1:
        return None
    r = a * b
    n = st(a) + st(b)
    ohne = int(dz(a).replace(",", "")) * int(dz(b).replace(",", ""))
    return mcq("%s %s %s = ?" % (dz(a), MAL, dz(b)), dz(r), [dz(r * 10), dz(r / 10), dz(Fr(ohne, 10 ** max(st(a), st(b)))) if Fr(ohne, 10 ** max(st(a), st(b))) != r else dz(r * 100)],
                   "Ohne Komma: %d %s %d = %d. Stellen nach dem Komma: %d + %d = %d. <b>%s</b>" % (int(dz(a).replace(",", "")), MAL, int(dz(b).replace(",", "")), ohne, st(a), st(b), n, dz(r)))


def durch_zahl():
    k = R.randint(2, 9)
    r = Fr(R.randint(11, 999), 10 ** R.randint(1, 2))
    v = r * k
    if r.denominator == 1 or st(v) > 3:
        return None
    return mcq("%s %s %d = ?" % (dz(v), G, k), dz(r), [dz(r * 10), dz(r / 10), dz(r + Fr(1, 10 ** max(st(r), 1)))],
               "Wie gewohnt dividieren. Beim Überschreiten des Kommas im Ergebnis das Komma setzen: <b>%s</b>. Probe: %s %s %d = %s." % (dz(r), dz(r), MAL, k, dz(v)))


def durch_dez():
    d = Fr(R.randint(2, 9), 10 ** R.randint(1, 2))
    r = Fr(R.randint(2, 60) * R.choice([1, 1, 10]), R.choice([1, 10]))
    v = r * d
    if st(v) > 3 or v < Fr(1, 10):
        return None
    k = st(d)
    return mcq("%s %s %s = ?" % (dz(v), G, dz(d)), dz(r), [dz(r / 10), dz(r * 10), dz(v * d) if v * d != r else None, dz(r / 100)],
               "Bei beiden Zahlen das Komma um %d Stelle%s nach rechts: %s %s %s = <b>%s</b>." % (k, "n" if k > 1 else "", dz(v * 10 ** k), G, dz(d * 10 ** k), dz(r)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["preis", "liter", "teilen", "flaeche", "benzin", "stueck"])
    if kind == "preis":
        pr = Fr(R.randint(45, 399), 100)
        k = R.randint(3, 12)
        t = pr * k
        f = lambda x: "%d,%02d €" % divmod(int(x * 100 + Fr(1, 2)), 100)
        return mcq("Ein Heft kostet %s. %s kauft %d Hefte. Wie viel muss %s bezahlen?" % (f(pr), p, k, er), f(t), [f(t / 10) if t >= 1 else f(t * 10), f(t + pr), f(t - Fr(1, 10))], "%s %s %d = <b>%s</b>." % (f(pr).replace(" €", ""), MAL, k, f(t)))
    if kind == "liter":
        pr = Fr(R.randint(80, 299), 100)
        l = Fr(R.randint(15, 60), 10)
        t = pr * l
        if (t * 100).denominator != 1:
            ex = Fr(int(t * 100 + Fr(1, 2)), 100)
        else:
            ex = t
        return mcq("Ein Liter Apfelsaft kostet %s €. Wie viel kosten %s Liter? (auf Cent runden)" % (dz(pr), dz(l)), "%d,%02d €" % divmod(int(ex * 100), 100),
                   ["%d,%02d €" % divmod(int(x * 100 + Fr(1, 2)), 100) for x in (ex * 10 if ex < 10 else ex / 10, ex + Fr(1, 10), pr + l)],
                   "%s %s %s = %s ≈ <b>%d,%02d €</b>." % ((dz(pr), MAL, dz(l), dz(t) if endlich(t) else "…") + divmod(int(ex * 100), 100)))
    if kind == "teilen":
        k = R.randint(3, 8)
        r = Fr(R.randint(150, 999), 100)
        t = r * k
        if (t * 100).denominator != 1:
            return None
        return mcq("%d Kinder teilen sich eine Rechnung von %s € gerecht. Wie viel zahlt jedes Kind?" % (k, dz(t)), "%d,%02d €" % divmod(int(r * 100), 100), ["%d,%02d €" % divmod(int(x * 100 + Fr(1, 2)), 100) for x in (r * 10, r + Fr(1, 10), t - k)],
                   "%s : %d = <b>%d,%02d €</b>." % ((dz(t), k) + divmod(int(r * 100), 100)))
    if kind == "flaeche":
        a, b = Fr(R.randint(12, 95), 10), Fr(R.randint(12, 95), 10)
        if a == b:
            return None
        return mcq("Ein Beet ist %s m lang und %s m breit. Wie groß ist die Fläche?" % (dz(a), dz(b)), "%s m²" % dz(a * b), ["%s m²" % dz(x) for x in (a * b * 10, a * b / 10, 2 * (a + b))],
                   "%s %s %s = <b>%s m²</b>." % (dz(a), MAL, dz(b), dz(a * b)))
    if kind == "benzin":
        v = Fr(R.randint(45, 75), 10)
        km = R.choice([100, 200, 300, 400, 50])
        r = v * km / 100
        return mcq("Ein Auto verbraucht %s Liter auf 100 km. Wie viele Liter braucht es für %d km?" % (dz(v), km), "%s l" % dz(r), ["%s l" % dz(x) for x in (v * km, r * 10, v + km / 100)],
                   "%s %s %s = <b>%s l</b>." % (dz(v), MAL, dz(Fr(km, 100)), dz(r)))
    d = Fr(R.choice([2, 4, 5, 25, 75]), 100) if R.random() < 0.5 else Fr(R.choice([2, 3, 4, 5]), 10)
    n = R.randint(4, 40)
    L = d * n
    return mcq("Eine %s m lange Schnur wird in Stücke von je %s m geschnitten. Wie viele Stücke entstehen?" % (dz(L), dz(d)), str(n), [str(n * 10), str(n // 10) if n >= 20 else str(n + 10), dz(L * d)],
               "%s %s %s = %s %s %s = <b>%d</b>." % (dz(L), G, dz(d), dz(L * 10 ** st(d)), G, dz(d * 10 ** st(d)), n))


def main():
    seen = set()
    sets = [
        ("Mal und durch 10, 100, 1000", mix(R, seen, [(zehner, 20)])),
        ("Dezimalzahl mal natürliche Zahl", mix(R, seen, [(mal_zahl, 12), (durch_zahl, 8)])),
        ("Dezimalzahl mal Dezimalzahl", mix(R, seen, [(mal_dez, 20)])),
        ("Durch eine Dezimalzahl teilen", mix(R, seen, [(durch_dez, 14), (durch_zahl, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Mal 10, 100, 1000</b>: Das Komma rückt 1, 2, 3 Stellen nach rechts. <b>Durch</b>: nach links.",
         "<b>Multiplizieren</b>: Erst ohne Komma rechnen. Das Ergebnis hat so viele Stellen nach dem Komma wie beide Faktoren zusammen.",
         "<b>Dividieren durch eine natürliche Zahl</b>: wie gewohnt; wenn man das Komma überschreitet, setzt man es im Ergebnis.",
         "<b>Dividieren durch eine Dezimalzahl</b>: Bei beiden Zahlen das Komma so weit nach rechts schieben, bis der Divisor eine natürliche Zahl ist."],
        [example("0,3 %s 0,2" % MAL, ["3 %s 2 = 6" % MAL, "1 + 1 = 2 Stellen"], "0,06"),
         example("4,8 %s 0,6" % G, ["Komma bei beiden um 1 Stelle: 48 %s 6" % G], "8")],
        [["0,3 %s 0,2 = 0,6" % MAL, "Zwei Stellen nach dem Komma: 0,06"],
         ["2,5 %s 100 = 0,025" % MAL, "Mal macht größer: 250"],
         ["4,8 %s 0,6 = 0,8" % G, "Komma bei beiden verschieben: 48 %s 6 = 8" % G]])
    faq = [
        {"q": "Wie multipliziert man zwei Dezimalzahlen?", "a": "Ohne Komma multiplizieren. Dann so viele Stellen abtrennen, wie beide Zahlen zusammen nach dem Komma haben: 1,2 · 0,3 = 0,36."},
        {"q": "Wie teilt man durch eine Dezimalzahl?", "a": "Bei beiden Zahlen das Komma gleich weit nach rechts verschieben, bis der Divisor ganz ist: 7,2 : 0,8 = 72 : 8 = 9."},
        {"q": "Warum wird das Ergebnis beim Multiplizieren manchmal kleiner?", "a": "Wenn man mit einer Zahl kleiner als 1 multipliziert, z. B. 5 · 0,4 = 2."},
        {"q": "Wohin rückt das Komma bei · 100?", "a": "Zwei Stellen nach rechts: 3,45 · 100 = 345."},
    ]
    make_unit(R, "dezimalzahlen-multiplizieren-und-dividieren", "Z",
              "Die Schülerinnen und Schüler multiplizieren und dividieren Dezimalzahlen mit Zehnerpotenzen, natürlichen Zahlen und Dezimalzahlen und lösen Sachaufgaben (Zusammenfassung).",
              "Dezimalzahlen multiplizieren und dividieren",
              "Dezimalzahlen multiplizieren und dividieren Klasse 6 – Arbeitsblätter",
              "Dezimalzahlen mal & geteilt",
              "Dezimalzahlen multiplizieren und dividieren für Klasse 6: Komma verschieben, Stellen zählen, durch Dezimalzahlen teilen, Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Multiplizieren: Stellen nach dem Komma zusammenzählen.",
              "Teilen durch eine Dezimalzahl: bei beiden Zahlen das Komma verschieben.",
              body, faq, sets, 10, grade="klasse-6")


if __name__ == "__main__":
    main()
