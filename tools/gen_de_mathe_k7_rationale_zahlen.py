# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Rationale Zahlen ordnen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k7_rationale_zahlen.py
Rationale Zahlen auf der Zahlengeraden, Betrag und Gegenzahl, Vergleichen und Ordnen (Brüche und Dezimalzahlen mit Vorzeichen), Zahlbereiche N, Z, Q, Abstände und Änderungen.
Fehler: −0,5 < −0,7 (wie bei positiven Zahlen gedacht), Betrag mit Gegenzahl verwechselt, ganze Zahlen nicht als rationale Zahlen erkannt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table, wrap, line, text, INK, RED
from de_k6 import bh, dz
from de_k7 import mcq

R = random.Random(49701)
KIDS = Kids(R)
LT, GT = "&lt;", "&gt;"


DEC = set()


def rz(dec=True):
    if dec:
        v = Fr(R.choice([-1, 1]) * R.randint(1, 99), R.choice([10, 100]))
        DEC.add(abs(v))
        return v
    n = R.choice([2, 3, 4, 5, 6, 8])
    z = R.randint(1, 3 * n)
    if z % n == 0:
        return None
    return Fr(R.choice([-1, 1]) * z, n)


def show(v, gem=True):
    v = Fr(v)
    return dz(v) if abs(v) in DEC or v.denominator == 1 else bh(v, gem)


def kl(v):
    return "(%s)" % dz(v) if v < 0 else dz(v)


def gerade():
    lo = R.randint(-4, -2)
    step = Fr(1, R.choice([2, 4, 5]))
    n = int(4 / step)
    i = R.randint(1, n - 1)
    v = lo + i * step
    if v == 0 or v.denominator == 1:
        return None
    W, x0, y = 340, 20, 50
    u = (W - 48) / float(n)
    s = [line(x0 - 6, y, x0 + n * u + 10, y, INK, 2)]
    for j in range(n + 1):
        big = (lo + j * step).denominator == 1
        s.append(line(x0 + j * u, y - (10 if big else 6), x0 + j * u, y + (10 if big else 6), INK, 2 if big else 1.2))
        if big:
            s.append(text(x0 + j * u, y + 30, dz(lo + j * step), 18))
    s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (x0 + i * u, y - 12, RED) + text(x0 + i * u, y - 27, "A", 18, col=RED))
    pic = wrap(W, y + 40, "".join(s), "Zahlengerade mit negativen Zahlen", lg=True)
    k = int(v) if v > 0 else int(v) - 1
    return mcq(pic + "Welche Zahl gehört zum Punkt A?", show(v), [show(-v), show(v + step), show(v - step), show(Fr(k) - (v - k))],
               "Zwischen zwei ganzen Zahlen sind %d Abschnitte, jeder ist %s. A liegt bei <b>%s</b>." % (int(1 / step), bh(step), show(v)))


def betrag():
    v = rz(R.random() < 0.6)
    if v is None:
        return None
    kind = R.choice(["betrag", "gegen", "beides"])
    if kind == "betrag":
        return mcq("Was ist |%s|?" % show(v), show(abs(v)), [show(-abs(v)), show(abs(v) + 1), "0"], "Der Betrag ist der Abstand zur 0, ohne Vorzeichen: <b>%s</b>." % show(abs(v)))
    if kind == "gegen":
        return mcq("Was ist die Gegenzahl von %s?" % show(v), show(-v), [show(v), show(-v + 1), show(v - 1)], "Gleicher Abstand zur 0, anderes Vorzeichen: <b>%s</b>." % show(-v))
    a, b = v, rz(True)
    if b is None or abs(a) == abs(b):
        return None
    big = a if abs(a) > abs(b) else b
    return mcq("Welche Zahl hat den größeren Betrag: %s oder %s?" % (show(a), show(b)), show(big), [show(b if big == a else a), "Beide gleich.", show(abs(big) * -1) if big > 0 else show(abs(big))],
               "|%s| = %s, |%s| = %s. <b>%s</b>" % (show(a), show(abs(a)), show(b), show(abs(b)), show(big)))


def vergleich():
    kind = R.choice(["dez", "dez", "bruch", "mix"])
    if kind == "dez":
        a = Fr(-R.randint(1, 99), R.choice([10, 100]))
        b = Fr(-R.randint(1, 99), R.choice([10, 100]))
        if R.random() < 0.3:
            b = -b
        DEC.update([abs(a), abs(b)])
    elif kind == "bruch":
        a, b = rz(False), rz(False)
        if a is None or b is None:
            return None
        if a > 0 and b > 0:
            a = -a
    else:
        a, b = rz(False), rz(True)
        if a is None:
            return None
    if a == b:
        return None
    s = LT if a < b else GT
    return mcq("Setze &lt;, &gt; oder = ein: %s ☐ %s" % (show(a), show(b)), s, [x for x in (LT, GT, "=") if x != s] + ["≈"],
               "Auf der Zahlengeraden liegt die kleinere Zahl weiter links. %s<b>%s %s %s</b>" % ("Bei negativen Zahlen ist die Zahl mit dem größeren Betrag kleiner. " if a < 0 and b < 0 else "", show(a), s, show(b)))


def ordnen():
    vals = set()
    while len(vals) < 4:
        v = rz(R.random() < 0.6)
        if v is not None:
            vals.add(v)
    vals = list(vals)
    if all(v > 0 for v in vals):
        return None
    srt = sorted(vals)
    ans = " &lt; ".join(show(v) for v in srt)
    bab = sorted(vals, key=lambda v: abs(v))
    cands = [" &lt; ".join(show(v) for v in x) for x in (bab, list(reversed(srt)), [srt[1], srt[0], srt[2], srt[3]], [srt[0], srt[2], srt[1], srt[3]])]
    return mcq("Ordne der Größe nach, beginne mit der kleinsten Zahl: %s" % "; ".join(show(v) for v in vals), ans, cands, "Von links nach rechts auf der Zahlengeraden: <b>%s</b>." % ans)


def bereiche():
    kind = R.choice(["welche", "gehoert", "zwischen"])
    if kind == "welche":
        S = [("−7", "Z und Q, aber nicht N"), ("12", "N, Z und Q"), (bh(Fr(-3, 4)), "nur Q"), ("0,5", "nur Q"), ("−2,5", "nur Q"), (bh(Fr(8, 2)) + " = 4", "N, Z und Q"), ("0", "Z und Q (in Deutschland meist auch N₀)")]
        x, a = R.choice(S[:6])
        return mcq("Zu welchen Zahlbereichen gehört die Zahl %s?" % x, a, [y for y in ("N, Z und Q", "Z und Q, aber nicht N", "nur Q", "nur N") if y != a], "N: natürliche Zahlen, Z: ganze Zahlen, Q: rationale Zahlen (alle Brüche). <b>%s</b>." % a)
    if kind == "gehoert":
        D = [("Welche Zahl ist eine ganze, aber keine natürliche Zahl?", "−5", ["5", "−0,5", bh(Fr(1, 2))]), ("Welche Zahl ist rational, aber nicht ganz?", "−1,25", ["−4", "0", "17"]),
             ("Welche Aussage stimmt?", "Jede ganze Zahl ist eine rationale Zahl.", ["Jede rationale Zahl ist eine ganze Zahl.", "Negative Zahlen sind keine rationalen Zahlen.", "0,5 ist eine ganze Zahl."]),
             ("Welche Zahl liegt genau in der Mitte zwischen −3 und 1?", "−1", ["−2", "0", "2"]), ("Welche Zahl liegt genau in der Mitte zwischen −2 und −1?", "−1,5", ["−1,2", "1,5", "−0,5"])]
        q, a, w = R.choice(D)
        return mcq(q, a, w, "<b>%s</b>." % a)
    a = Fr(R.randint(-30, 10), 10)
    b = a + Fr(R.randint(2, 20), 10)
    m = (a + b) / 2
    return mcq("Welche Zahl liegt genau in der Mitte zwischen %s und %s?" % (dz(a), dz(b)), dz(m), [dz((b - a) / 2), dz(m + Fr(1, 10)), dz(-m) if m else "1"],
               "(%s + %s) : 2 = <b>%s</b>." % (dz(a), kl(b), dz(m)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["temp", "konto", "tauchen", "pegel", "aktie"])
    if kind == "temp":
        st = ["Moskau", "Oslo", "Berlin", "Helsinki", "Zugspitze"]
        t = {s: Fr(R.randint(-150, 40), 10) for s in R.sample(st, 4)}
        if len(set(t.values())) < 4:
            return None
        kalt = min(t, key=t.get)
        return mcq("Temperaturen am Morgen: %s. Wo ist es am kältesten?" % ", ".join("%s %s °C" % (s, dz(v)) for s, v in t.items()), kalt, [s for s in t if s != kalt],
                   "Die kleinste Zahl ist %s °C: <b>%s</b>." % (dz(t[kalt]), kalt))
    if kind == "konto":
        a, b = Fr(R.randint(-9000, -500), 100), Fr(R.randint(-9000, 2000), 100)
        if a == b:
            return None
        d = abs(a - b)
        return mcq("Der Kontostand von %s war %s € und ist jetzt %s €. Um wie viel Euro hat er sich verändert?" % (p, dz(a), dz(b)), "um %s €" % dz(d), ["um %s €" % dz(x) for x in (abs(abs(a) - abs(b)) if abs(abs(a) - abs(b)) != d else d + 10, abs(a) + abs(b) if abs(a) + abs(b) != d else d / 2, d + 1)],
                   "|%s − %s| = <b>%s €</b>." % (dz(b), kl(a), dz(d)))
    if kind == "tauchen":
        a, b = Fr(-R.randint(15, 120), 10), Fr(-R.randint(15, 120), 10)
        if a == b:
            return None
        d = abs(a - b)
        return mcq("Ein Taucher ist bei %s m. Später ist er bei %s m. Wie viele Meter ist er %s?" % (dz(a), dz(b), "aufgestiegen" if b > a else "abgetaucht"), "%s m" % dz(d), ["%s m" % dz(x) for x in (abs(a) + abs(b), d + 1, d * 2)],
                   "|%s − %s| = <b>%s m</b>." % (dz(b), kl(a), dz(d)))
    if kind == "pegel":
        vals = [Fr(R.randint(-25, 25), 10) for _ in range(4)]
        if len(set(vals)) < 4:
            return None
        sp = max(vals) - min(vals)
        return mcq("Ein Pegel zeigt an vier Tagen: %s m. Wie groß ist der Unterschied zwischen dem höchsten und dem niedrigsten Wert?" % "; ".join(dz(v) for v in vals), "%s m" % dz(sp), ["%s m" % dz(x) for x in (max(vals) + min(vals) if max(vals) + min(vals) > 0 else sp + 1, max(vals), sp / 2)],
                   "%s − %s = <b>%s m</b>." % (dz(max(vals)), kl(min(vals)), dz(sp)))
    a = Fr(R.randint(-50, 50), 10)
    if a == 0:
        return None
    b = Fr(R.randint(-50, 50), 10)
    s = a + b
    return mcq("Eine Aktie ändert sich am Montag um %s € und am Dienstag um %s €. Wie groß ist die Änderung insgesamt?" % (dz(a), dz(b)), "%s €" % dz(s), ["%s €" % dz(x) for x in (a - b, abs(a) + abs(b), -s if s else 1)],
               "%s + %s = <b>%s €</b>." % (dz(a), kl(b), dz(s)))


def main():
    seen = set()
    sets = [
        ("Zahlengerade", mix(R, seen, [(gerade, 20)])),
        ("Betrag und Gegenzahl", mix(R, seen, [(betrag, 20)])),
        ("Vergleichen", mix(R, seen, [(vergleich, 20)])),
        ("Ordnen und Zahlbereiche", mix(R, seen, [(ordnen, 12), (bereiche, 8)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Rationale Zahlen</b> (Q) sind alle Zahlen, die man als Bruch schreiben kann – positive, negative und die 0: −%s, −2,5, 0, 7." % fr(3, 4),
         "Auf der <b>Zahlengeraden</b> ist eine Zahl kleiner, wenn sie weiter links liegt.",
         "Bei zwei negativen Zahlen ist die Zahl mit dem größeren <b>Betrag</b> die kleinere: −0,7 &lt; −0,5.",
         "N ⊂ Z ⊂ Q: Jede natürliche Zahl ist ganz, jede ganze Zahl ist rational."],
        [example("−0,7 ☐ −0,5", ["|−0,7| = 0,7 ist größer", "−0,7 liegt weiter links"], "−0,7 &lt; −0,5"),
         example("Mitte zwischen −3 und 1", ["(−3 + 1) : 2"], "−1")],
        [["−0,5 &lt; −0,7, weil 5 &lt; 7", "−0,7 liegt weiter links: −0,7 &lt; −0,5"],
         ["|−3| = −3", "Der Betrag ist nie negativ: 3"],
         ["−4 ist keine rationale Zahl", "Jede ganze Zahl ist rational: −4 = −4/1"]])
    faq = [
        {"q": "Was sind rationale Zahlen?", "a": "Alle Zahlen, die man als Bruch zweier ganzer Zahlen schreiben kann: positive und negative Brüche, Dezimalzahlen mit Ende oder Periode und die ganzen Zahlen."},
        {"q": "Wie vergleicht man negative Zahlen?", "a": "Die Zahl, die auf der Zahlengeraden weiter links liegt, ist kleiner. Bei negativen Zahlen ist das die mit dem größeren Betrag."},
        {"q": "Was ist der Betrag einer Zahl?", "a": "Ihr Abstand zur 0. |−2,5| = 2,5."},
        {"q": "Was bedeuten N, Z und Q?", "a": "N: natürliche Zahlen (1, 2, 3 …), Z: ganze Zahlen (… −1, 0, 1 …), Q: rationale Zahlen (alle Brüche mit Vorzeichen)."},
    ]
    make_unit(R, "rationale-zahlen", "Z",
              "Die Schülerinnen und Schüler stellen rationale Zahlen auf der Zahlengeraden dar, bestimmen Betrag und Gegenzahl, vergleichen und ordnen rationale Zahlen und unterscheiden die Zahlbereiche N, Z und Q (Zusammenfassung).",
              "Rationale Zahlen ordnen",
              "Rationale Zahlen Klasse 7 – vergleichen und ordnen, Arbeitsblätter",
              "Rationale Zahlen",
              "Rationale Zahlen für Klasse 7: Zahlengerade, Betrag und Gegenzahl, vergleichen und ordnen, Zahlbereiche. 100 Aufgaben mit Lösungen, kostenlos.",
              "Weiter links ist kleiner.",
              "Bei negativen Zahlen: größerer Betrag, kleinere Zahl.",
              body, faq, sets, 1, grade="klasse-7")


if __name__ == "__main__":
    main()
