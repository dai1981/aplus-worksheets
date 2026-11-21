# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Zahlen bis 1 Million（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k4_zahlen_bis_1_million.py
Stellenwerttafel (HT ZT T H Z E), Zahlwörter, Wert einer Ziffer, Zahlenstrahl, Nachbarzahlen, vergleichen und Sachaufgaben.
Fehler: Null vergessen (dreihunderttausendvier → 3004), Ziffernwert mit Ziffer verwechselt, Skala falsch gelesen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, zahlenstrahl, stellentafel, wort, Kids

R = random.Random(49101)
KIDS = Kids(R)
NAMEN = ["Hunderttausender", "Zehntausender", "Tausender", "Hunderter", "Zehner", "Einer"]


def six():
    return R.randint(100001, 999999)


def drop0(n):
    s = str(n).replace("0", "")
    return int(s) if s and s != str(n) else None


def tafel():
    n = six()
    if R.random() < 0.4:
        s = list(str(n))
        for k in R.sample(range(1, 6), 2):
            s[k] = "0"
        n = int("".join(s))
    w = [drop0(n), n * 10 if n * 10 < 10 ** 6 else None, n // 10, n + 10000 if n < 990000 else n - 20000, n - 1000]
    return mcq("Welche Zahl steht in der Stellenwerttafel?" + stellentafel(n), num(n), [num(x) for x in w if x and x != n and x > 0],
               "HT = Hunderttausender, ZT = Zehntausender, T = Tausender. Leere Stellen gibt es nicht: Es steht dort eine 0. Die Zahl ist <b>%s</b>." % num(n))


def zahlwort():
    n = six()
    if R.random() < 0.4:
        n = n // 1000 * 1000 + R.choice([0, R.randint(1, 99), R.randint(1, 9)])
    t, r = divmod(n, 1000)
    w = [int("%d%d" % (t, r)) if r else t, t * 1000 + int(str(r)[::-1]) if r >= 10 and str(r)[::-1] != str(r) else None,
         n + 100000 if n < 900000 else n - 100000, n + 10, t * 100 + r if r < 100 else None]
    return mcq("Schreibe mit Ziffern: <b>%s</b>" % wort(n), num(n), [num(x) for x in w if x and x != n and 0 < x < 1000000],
               "Erst der Tausenderteil (%s = %s), dann der Rest (%s). Fehlende Stellen werden mit 0 gefüllt: <b>%s</b>." % (wort(t) if t else "null", num(t), wort(r) if r else "nichts", num(n)))


def lesen():
    n = six()
    w = [wort(n + 10000) if n < 990000 else wort(n - 10000), wort(n // 1000 * 1000 + (n % 1000 + 100) % 1000), wort(int(str(n)[:3][::-1] + str(n)[3:])) if str(n)[:3][::-1] != str(n)[:3] and str(n)[2] != "0" else wort(n + 1)]
    return mcq("Wie heißt die Zahl <b>%s</b>?" % num(n), wort(n), w, "%s: zuerst %s-tausend, dann %s. Richtig: <b>%s</b>." % (num(n), wort(n // 1000).replace("eins", "ein"), wort(n % 1000) if n % 1000 else "nichts", wort(n)))


def ziffernwert():
    n = six()
    s = str(n)
    k = R.randint(0, 5)
    d = int(s[k])
    if d == 0 or s.count(s[k]) > 1:
        return None
    val = d * 10 ** (5 - k)
    w = [d, d * 10 ** (4 - k) if k < 5 else d * 10, d * 10 ** (6 - k), d * 100 if val != d * 100 else d * 1000]
    return mcq("Welchen Wert hat die Ziffer %d in der Zahl %s?" % (d, num(n)), num(val), [num(x) for x in w if x != val],
               "Die %d steht bei den %s: %d %s = <b>%s</b>." % (d, NAMEN[k], d, NAMEN[k], num(val)))


def zerlegen():
    n = six()
    parts = [int(c) * 10 ** (5 - i) for i, c in enumerate(str(n)) if c != "0"]
    if len(parts) < 4:
        return None
    sh = parts[:]
    R.shuffle(sh)
    w = [drop0(n), n + 1000, n - 10, int("".join(str(int(c)) for c in str(n)[::-1])) if str(n)[::-1][0] != "0" else n + 100]
    return mcq("%s = ?" % " + ".join(num(p) for p in sh), num(n), [num(x) for x in w if x and x != n and 0 < x < 1000000],
               "Ordne nach Stellenwerten: <b>%s</b>." % num(n))


def strahl():
    kind = R.choice(["ht", "zt", "t"])
    if kind == "ht":
        v = R.randint(1, 9) * 100000
        if v == 500000:
            return None
        lo, hi, step, every, lab = 0, 1000000, 100000, 500000, [0, 500000, 1000000]
        w = [v + 100000, v - 100000, v // 10, v + 50000]
    elif kind == "zt":
        lo = R.randint(0, 9) * 100000
        hi, step, every = lo + 100000, 10000, 50000
        v = lo + R.choice([1, 2, 3, 4, 6, 7, 8, 9]) * 10000
        lab = [lo, lo + 50000, hi]
        w = [v + 10000, v - 10000, lo + (v - lo) // 10, v + 1000]
    else:
        lo = R.randint(10, 99) * 10000
        hi, step, every = lo + 10000, 1000, 5000
        v = lo + R.choice([1, 2, 3, 4, 6, 7, 8, 9]) * 1000
        lab = [lo, lo + 5000, hi]
        w = [v + 1000, v - 1000, lo + (v - lo) // 10, v + 100]
    pic = zahlenstrahl(lo, hi, step, marks=[(v, "?")], labels=lab, every=every)
    return mcq(pic + "Welche Zahl gehört an den Pfeil?", num(v), [num(x) for x in w if 0 <= x <= 1000000 and x != v],
               "Ein Strich bedeutet %s. Zähle von %s aus weiter: <b>%s</b>." % (num(step), num(lab[0] if v < lab[1] else lab[1]), num(v)))


def nachbar():
    n = six()
    kind = R.choice(["T", "ZT", "HT", "vor", "nach"])
    if kind == "vor":
        n = n // 1000 * 1000
        return mcq("Welche Zahl ist der Vorgänger von %s?" % num(n), num(n - 1), [num(x) for x in (n + 1, n - 10, n - 1000, n - 11)],
                   "Der Vorgänger ist um 1 kleiner: %s − 1 = <b>%s</b>." % (num(n), num(n - 1)))
    if kind == "nach":
        n = n // 1000 * 1000 + 999
        return mcq("Welche Zahl ist der Nachfolger von %s?" % num(n), num(n + 1), [num(x) for x in (n - 1, n + 10, n - 899, n + 1001)],
                   "Der Nachfolger ist um 1 größer: %s + 1 = <b>%s</b>." % (num(n), num(n + 1)))
    step = {"T": 1000, "ZT": 10000, "HT": 100000}[kind]
    word = {"T": "Nachbartausendern", "ZT": "Nachbarzehntausendern", "HT": "Nachbarhunderttausendern"}[kind]
    if n % step == 0:
        return None
    lo = n // step * step
    ans = "%s und %s" % (num(lo), num(lo + step))
    o = {"T": 10000, "ZT": 1000, "HT": 10000}[kind]
    w = ["%s und %s" % (num(n // o * o), num(n // o * o + o)), "%s und %s" % (num(lo - step), num(lo)) if lo >= step else "%s und %s" % (num(lo + step), num(lo + 2 * step)),
         "%s und %s" % (num(n - 1), num(n + 1))]
    return mcq("Zwischen welchen %s liegt %s?" % (word, num(n)), ans, w, "Direkt davor und danach: <b>%s</b>." % ans)


def sache():
    kind = R.choice(["groesste", "kleinste", "mehr", "rätsel"])
    if kind in ("groesste", "kleinste"):
        base = R.randint(10, 99) * 10000
        ns = list({base + R.randint(0, 9999) for _ in range(4)})
        if len(ns) < 4:
            return None
        big = kind == "groesste"
        orte = R.sample(["Ahornstadt", "Birkenfeld", "Eichental", "Lindenhausen", "Tannenberg", "Ulmenhof"], 4)
        q = "Einwohner in vier Städten: %s. Welche Stadt hat die %s Einwohner?" % (", ".join("%s %s" % (o, num(n)) for o, n in zip(orte, ns)), "meisten" if big else "wenigsten")
        k = ns.index(max(ns) if big else min(ns))
        return mcq(q, orte[k], [o for i, o in enumerate(orte) if i != k], "Vergleiche von vorne Stelle für Stelle. Richtig: <b>%s</b> (%s)." % (orte[k], num(ns[k])))
    if kind == "mehr":
        a = R.randint(20, 90) * 1000
        s = R.choice([1000, 10000, 100000])
        q = "Ein Stadion hat %s Plätze. Ein neues Stadion soll %s Plätze mehr haben. Wie viele Plätze hat das neue Stadion?" % (num(a), num(s))
        r = a + s
        return mcq(q, num(r), [num(x) for x in (a + s // 10, a + s * 10 if a + s * 10 < 10 ** 6 else a - s, r + 1000 if s != 1000 else r + 100)], "%s + %s = <b>%s</b>." % (num(a), num(s), num(r)))
    ht, zt, t = R.sample(range(1, 10), 3)
    n = ht * 100000 + zt * 10000 + t * 1000
    q = "Meine Zahl hat %d Hunderttausender, %d Tausender und %d Zehntausender. Sonst nur Nullen. Welche Zahl ist es?" % (ht, t, zt)
    w = [ht * 100000 + t * 10000 + zt * 1000, ht * 1000 + t * 100 + zt * 10, n // 10]
    return mcq(q, num(n), [num(x) for x in w if x != n], "HT = %d, ZT = %d, T = %d, H = Z = E = 0: <b>%s</b>." % (ht, zt, t, num(n)))


def main():
    seen = set()
    sets = [
        ("Die Stellenwerttafel", mix(R, seen, [(tafel, 12), (ziffernwert, 8)])),
        ("Zahlen lesen und schreiben", mix(R, seen, [(zahlwort, 12), (lesen, 8)])),
        ("Zahlen zerlegen", mix(R, seen, [(zerlegen, 12), (ziffernwert, 8)])),
        ("Zahlenstrahl und Nachbarzahlen", mix(R, seen, [(strahl, 12), (nachbar, 8)])),
        ("Zahlenrätsel und Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Im Zahlenraum bis zur Million gibt es sechs Stellen: <b>HT</b> (Hunderttausender), <b>ZT</b> (Zehntausender), <b>T</b> (Tausender), H, Z und E.",
         "Große Zahlen schreibt man in Dreiergruppen mit einem kleinen Abstand: 345 206.",
         "Beim Lesen sagst du zuerst den Tausenderteil, dann den Rest: dreihundertfünfundvierzig<b>tausend</b>zweihundertsechs.",
         "Fehlt eine Stelle, steht dort eine 0: dreihunderttausendvier = 300 004."],
        [example("Schreibe mit Ziffern: zweihundertsiebentausendfünfzig", ["Tausenderteil: 207", "Rest: 050"], "207 050"),
         example("Welchen Wert hat die 6 in 462 135?", ["Die 6 steht bei den Zehntausendern"], "60 000")],
        [["dreihunderttausendvier → 3004", "Alle Nullen schreiben: 300 004"],
         ["Wert der 6 in 462 135 → 6", "Der Wert hängt von der Stelle ab: 60 000"],
         ["Am Zahlenstrahl jeden Strich als 1 000 zählen", "Erst die Schrittweite bestimmen"]],
        extra=stellentafel(345206))
    faq = [
        {"q": "Bis zu welcher Zahl rechnen Kinder in Klasse 4?", "a": "In Klasse 4 wird der Zahlenraum bis zu einer Million erschlossen: lesen, schreiben, ordnen, runden und schriftlich rechnen."},
        {"q": "Warum schreibt man große Zahlen in Dreiergruppen?", "a": "So lassen sie sich leichter lesen: 345 206 statt 345206. Man liest zuerst die Tausendergruppe, dann den Rest."},
        {"q": "Wie stellt man sich eine Million vor?", "a": "Zum Beispiel als 1000 Pakete mit je 1000 Blatt Papier oder als die Einwohnerzahl einer großen Stadt."},
        {"q": "Was ist der Unterschied zwischen Ziffer und Zahl?", "a": "Ziffern sind die Zeichen 0 bis 9. Eine Zahl kann aus mehreren Ziffern bestehen; der Wert einer Ziffer hängt von ihrer Stelle ab."},
    ]
    make_unit(R, "zahlen-bis-1-million", "Z",
              "Die Schülerinnen und Schüler verstehen den Aufbau des Zehnersystems im Zahlenraum bis zur Million, lesen, schreiben und zerlegen Zahlen und ordnen sie am Zahlenstrahl ein (Zusammenfassung).",
              "Zahlen bis 1 Million: Stellenwerte und Zahlwörter",
              "Zahlen bis 1 Million – Mathe Klasse 4 Arbeitsblätter mit Lösungen",
              "Zahlen bis 1 Million",
              "Mathe Klasse 4: Zahlen bis zur Million mit Stellenwerttafel, Zahlwörtern, Wert einer Ziffer, Zahlenstrahl und Nachbarzahlen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "HT, ZT, T, H, Z, E – jede Ziffer hat ihren Platz.",
              "Große Zahlen in Dreiergruppen lesen: erst den Tausenderteil, dann den Rest.",
              body, faq, sets, 1, grade="klasse-4")


if __name__ == "__main__":
    main()
