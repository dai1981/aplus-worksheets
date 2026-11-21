# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Runden und Überschlagen bis 1 Million（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k4_runden_und_ueberschlagen.py
Runden auf Hunderter, Tausender, Zehntausender und Hunderttausender, welche Zahl wird so gerundet, Überschlag, Sachaufgaben.
Fehler: immer abrunden, auf die falsche Stelle runden, beim Aufrunden über die 9 (39 600 → 30 000 statt 40 000).
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL

R = random.Random(49102)
KIDS = Kids(R)
STUFE = [(100, "Hunderter"), (1000, "Tausender"), (10000, "Zehntausender"), (100000, "Hunderttausender")]


def rd(n, s):
    return (n + s // 2) // s * s


def runden(levels):
    def mk():
        s, name = R.choice(levels)
        n = R.randint(1001, 989999)
        if n % s == 0:
            return None
        if R.random() < 0.3:   # über die 9
            n = n // (s * 10) * (s * 10) + 9 * s + R.randint(s // 2, s - 1)
            if n >= 1000000:
                return None
        a = rd(n, s)
        down, up = n // s * s, n // s * s + s
        w = [down if a == up else up, rd(n, s * 10) if rd(n, s * 10) != a else None, rd(n, s // 10) if s > 10 else n, a + s, a - s,
             n // (s * 10) * (s * 10) if a == up and a % (s * 10) == 0 else None, a + 2 * s, rd(n, s // 100) if s >= 1000 else None]
        dig = n // (s // 10) % 10
        return mcq("Runde %s auf %s." % (num(n), name), num(a), [num(x) for x in w if x is not None and x > 0 and x != a],
                   "Schau auf die Stelle rechts von den %sn: %d. %s %s ≈ <b>%s</b>."
                   % (name, dig, "Bei 5 bis 9 rundest du auf." if dig >= 5 else "Bei 0 bis 4 rundest du ab.", num(n), num(a)))
    return mk


def welche():
    s, name = R.choice(STUFE[1:3])
    t = R.randint(2, 98) * s
    ok = t - s // 2 + R.randint(0, s - 1)
    bad = [t - s // 2 - R.randint(1, s // 4), t + s // 2 + R.randint(0, s // 4), t + s + R.randint(-s // 3, s // 3)]
    bad = [b for b in bad if rd(b, s) != t and b > 0]
    if rd(ok, s) != t or ok == t or len(set(bad)) < 3:
        return None
    return mcq("Welche Zahl ergibt auf %s gerundet %s?" % (name, num(t)), num(ok), [num(b) for b in bad],
               "%s ≈ %s. Die anderen werden zu %s gerundet." % (num(ok), num(t), ", ".join(num(rd(b, s)) for b in bad)))


def ueberschlag():
    op = R.choice(["+", "−", MAL])
    if op == MAL:
        a = R.randint(110, 980)
        b = R.randint(3, 9)
        ra = rd(a, 100)
        est, exact = ra * b, a * b
        q = "Überschlage: %s %s %d ≈ ?" % (num(a), MAL, b)
        e = "Runde %s auf %s: %s %s %d = <b>%s</b>. (Genau: %s)" % (num(a), num(ra), num(ra), MAL, b, num(est), num(exact))
        w = [exact, est + ra, est - ra, rd(a, 10) * b]
    else:
        a = R.randint(12000, 680000)
        b = R.randint(11000, 300000) if op == "+" else R.randint(11000, a - 5000)
        s = 10000 if max(a, b) < 100000 else 100000 if R.random() < 0.3 else 10000
        ra, rb = rd(a, s), rd(b, s)
        est = ra + rb if op == "+" else ra - rb
        exact = a + b if op == "+" else a - b
        if est <= 0:
            return None
        q = "Überschlage auf %s: %s %s %s ≈ ?" % ("Zehntausender" if s == 10000 else "Hunderttausender", num(a), op, num(b))
        e = "%s %s %s = <b>%s</b>. (Genau: %s)" % (num(ra), op, num(rb), num(est), num(exact))
        w = [exact, est + s, est - s, rd(a, s * 10) + rd(b, s * 10) if op == "+" else rd(a, s * 10) - rd(b, s * 10), est + 2 * s, rd(exact, s // 10)]
    if est == exact:
        return None
    return mcq(q, num(est), [num(x) for x in w if x > 0 and x != est], e)


ORTE = ["Ahornstadt", "Birkenfeld", "Eichental", "Lindenhausen", "Tannenberg", "Ulmenhof", "Weidenau"]


def sache():
    kind = R.choice(["einwohner", "einwohner", "zuschauer", "reicht"])
    if kind == "einwohner":
        o = R.choice(ORTE)
        n = R.randint(12000, 980000)
        s, name = R.choice(STUFE[1:4] if n > 100000 else STUFE[1:3])
        a = rd(n, s)
        if a == n:
            return None
        q = "%s hat %s Einwohner. In der Zeitung steht die Zahl auf %s gerundet. Welche Zahl steht dort?" % (o, num(n), name)
        w = [n // s * s if a != n // s * s else n // s * s + s, rd(n, s * 10) if rd(n, s * 10) != a else a + s, a + s, rd(n, s // 10)]
        return mcq(q, "etwa %s" % num(a), ["etwa %s" % num(x) for x in w if x != a], "%s ≈ <b>%s</b>." % (num(n), num(a)))
    if kind == "zuschauer":
        sp = [R.randint(18000, 49000) for _ in range(3)]
        est = sum(rd(x, 1000) for x in sp)
        q = "Bei drei Heimspielen kamen %s, %s und %s Zuschauer. Etwa wie viele waren es zusammen? Runde auf Tausender." % tuple(num(x) for x in sp)
        if est == sum(sp):
            return None
        return mcq(q, "etwa %s" % num(est), ["etwa %s" % num(x) for x in (sum(sp), est + 1000, est - 1000, sum(rd(x, 10000) for x in sp)) if x != est],
                   "%s ≈ <b>%s</b>." % (" + ".join(num(rd(x, 1000)) for x in sp), num(est)))
    p = KIDS.next()
    price = R.randint(210, 890)
    n = R.randint(3, 9)
    budget = rd(price * n, 1000) + R.choice([-1000, 1000])
    ok = price * n <= budget
    q = "Eine Schule möchte %d Tablets zu je %s € kaufen. Sie hat %s €. Reicht das Geld? Überschlage." % (n, num(price), num(budget))
    ans = "Ja, etwa %s € reichen." % num(rd(price, 100) * n) if ok else "Nein, es kostet etwa %s €." % num(rd(price, 100) * n)
    w = ["Nein, es kostet etwa %s €." % num(rd(price, 100) * n) if ok else "Ja, etwa %s € reichen." % num(rd(price, 100) * n),
         "Ja, etwa %s € reichen." % num(rd(price, 100) * n + 1000), "Nein, es kostet etwa %s €." % num(rd(price, 100) * n + 1000)]
    if (rd(price, 100) * n <= budget) != ok:
        return None
    return mcq(q, ans, w, "Überschlag: %s %s %d = %s €. Genau: %s €. %s" % (num(rd(price, 100)), MAL, n, num(rd(price, 100) * n), num(price * n),
                                                                          "Das passt in %s €." % num(budget) if ok else "Das ist mehr als %s €." % num(budget)))


def main():
    seen = set()
    sets = [
        ("Runden auf Hunderter und Tausender", mix(R, seen, [(runden(STUFE[:2]), 20)])),
        ("Runden auf Zehn- und Hunderttausender", mix(R, seen, [(runden(STUFE[2:]), 20)])),
        ("Welche Zahl wird so gerundet?", mix(R, seen, [(welche, 14), (runden(STUFE), 6)])),
        ("Überschlagen", mix(R, seen, [(ueberschlag, 20)])),
        ("Sachaufgaben zum Runden", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Beim Runden schaust du auf die Stelle <b>rechts</b> von der Rundungsstelle.",
         "Bei 0, 1, 2, 3, 4 rundest du ab, bei 5, 6, 7, 8, 9 rundest du auf.",
         "Wird beim Aufrunden aus einer 9 eine 10, wandert die 1 eine Stelle weiter: 39 600 ≈ 40 000 (auf Tausender).",
         "Beim <b>Überschlag</b> rundest du zuerst und rechnest dann im Kopf. So prüfst du Ergebnisse."],
        [example("Runde 284 517 auf Zehntausender.", ["Zehntausender: 8, rechts davon 4", "4 → abrunden"], "280 000"),
         example("Überschlage 38 400 + 51 700.", ["38 400 ≈ 38 000, 51 700 ≈ 52 000", "38 000 + 52 000 = 90 000"], "etwa 90 000")],
        [["284 517 auf ZT → 290 000", "Rechts von der 8 steht eine 4: abrunden → 280 000"],
         ["39 600 auf T → 30 000", "9 + 1 = 10: 40 000"],
         ["Auf die falsche Stelle runden", "Erst die Rundungsstelle markieren"]])
    faq = [
        {"q": "Warum lernt man Runden mit großen Zahlen?", "a": "Große Zahlen wie Einwohnerzahlen oder Zuschauer werden im Alltag fast immer gerundet angegeben. Gerundete Zahlen kann man sich leichter merken und vergleichen."},
        {"q": "Was ist der Unterschied zwischen Runden und Überschlagen?", "a": "Runden macht aus einer Zahl eine glatte Zahl. Überschlagen heißt: erst runden, dann mit den gerundeten Zahlen rechnen."},
        {"q": "Was passiert bei 999 500 auf Tausender?", "a": "Es wird aufgerundet auf 1 000 000, also eine Million."},
        {"q": "Wann sollte man einen Überschlag machen?", "a": "Vor jeder schriftlichen Rechnung. So erkennt man große Fehler sofort."},
    ]
    make_unit(R, "runden-und-ueberschlagen", "Z",
              "Die Schülerinnen und Schüler runden Zahlen bis zur Million sachgerecht, nutzen Überschläge zur Kontrolle und arbeiten mit gerundeten Angaben in Sachsituationen (Zusammenfassung).",
              "Runden und Überschlagen bis 1 Million",
              "Runden Klasse 4 – auf Tausender und Zehntausender, Arbeitsblätter mit Lösungen",
              "Runden und Überschlagen",
              "Mathe Klasse 4: Runden auf Hunderter, Tausender, Zehntausender und Hunderttausender, Überschlag und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "0 bis 4 abrunden, 5 bis 9 aufrunden.",
              "Schau immer auf die Stelle rechts von der Rundungsstelle.",
              body, faq, sets, 2, grade="klasse-4")


if __name__ == "__main__":
    main()
