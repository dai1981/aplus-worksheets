# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Dezimalzahlen und Stellenwerte（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_dezimalzahlen_und_stellenwerte.py
Zehntel, Hundertstel, Tausendstel, Stellenwerttafel, Dezimalzahlen vergleichen und ordnen, Zahlenstrahl, Runden, Größen in Kommaschreibweise.
Fehler: 0,45 > 0,5 (weil 45 > 5), Endnullen falsch gedeutet, Stellen nach dem Komma als Ganze gelesen, falsch gerundet.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table, wrap, line, text, INK, RED
from de_k6 import dz, mcq

R = random.Random(49607)
KIDS = Kids(R)
LT, GT = "&lt;", "&gt;"
ST = ["Zehntel", "Hundertstel", "Tausendstel"]


def zufall(st=3, maxg=99):
    g = R.randint(0, maxg)
    k = R.randint(1, st)
    n = R.randint(1, 10 ** k - 1)
    if n % 10 == 0:
        return None
    return Fr(g) + Fr(n, 10 ** k)


def stelle():
    v = zufall(3, 999)
    if v is None:
        return None
    s = dz(v)
    ip, fp = s.split(",")
    fp = fp.ljust(3, "0")
    i = R.randint(0, 2)
    d = int(fp[i])
    if d == 0:
        return None
    wrong = ["%d %s" % (d, ST[j]) for j in range(3) if j != i] + ["%d Zehner" % d, "%d Einer" % d]
    return mcq("Welchen Wert hat die Ziffer %d an der %d. Stelle nach dem Komma in %s?" % (d, i + 1, s), "%d %s" % (d, ST[i]), wrong,
               "1. Stelle nach dem Komma: Zehntel, 2. Stelle: Hundertstel, 3. Stelle: Tausendstel. <b>%d %s</b>." % (d, ST[i]))


def schreiben():
    kind = R.choice(["bruch", "wort", "zerlegt"])
    if kind == "bruch":
        k = R.randint(1, 3)
        n = R.randint(1, 10 ** k - 1)
        if n % 10 == 0:
            return None
        v = Fr(n, 10 ** k)
        wrong = [dz(Fr(n, 10 ** (k + 1))), dz(Fr(n, 10 ** (k - 1))) if k > 1 else "%d,0" % n, "%d,%d" % (n, 10 ** k)]
        return mcq("Schreibe als Dezimalzahl: %s" % fr(n, 10 ** k), dz(v), wrong, "Der Nenner %d hat %d Null%s, also %d Stelle%s nach dem Komma: <b>%s</b>." % (10 ** k, k, "en" if k > 1 else "", k, "n" if k > 1 else "", dz(v)))
    if kind == "wort":
        e, z, h = R.randint(0, 20), R.randint(0, 9), R.randint(1, 9)
        v = e + Fr(z, 10) + Fr(h, 100)
        return mcq("Schreibe als Dezimalzahl: %d Einer, %d Zehntel und %d Hundertstel" % (e, z, h), dz(v), [dz(e + Fr(h, 10) + Fr(z, 100)) if z != h else dz(v + Fr(1, 10)), "%d,%d0%d" % (e, z, h), dz(e + Fr(z, 100) + Fr(h, 1000))],
                   "<b>%s</b>" % dz(v))
    e, z, t = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
    v = e + Fr(z, 10) + Fr(t, 1000)
    return mcq("Schreibe als Dezimalzahl: %d + %s + %s" % (e, fr(z, 10), fr(t, 1000)), dz(v), ["%d,%d%d" % (e, z, t), dz(e + Fr(z, 10) + Fr(t, 100)), dz(e + Fr(z, 100) + Fr(t, 1000))],
               "Die Hundertstel fehlen, dort steht eine 0: <b>%s</b>." % dz(v))


def vergleich():
    while True:
        a = Fr(R.randint(0, 9)) + Fr(R.randint(1, 9), 10)
        kind = R.choice(["laenge", "laenge", "nah"])
        if kind == "laenge":
            b = Fr(int(a * 10) - 1, 10) + Fr(R.randint(11, 99), 1000)
        else:
            b = a + Fr(R.choice([-1, 1]) * R.randint(1, 9), 100)
        if b > 0 and a != b:
            break
    x, y = (a, b) if R.random() < 0.5 else (b, a)
    s = LT if x < y else GT
    return mcq("Setze &lt;, &gt; oder = ein: %s ☐ %s" % (dz(x), dz(y)), s, [t for t in (LT, GT, "=") if t != s] + ["≈"],
               "Stelle für Stelle von links vergleichen (gleich viele Stellen nach dem Komma helfen): <b>%s %s %s</b>." % (dz(x), s, dz(y)))


def ordnen():
    g = R.randint(0, 5)
    vals = set()
    while len(vals) < 4:
        k = R.randint(1, 3)
        n = R.randint(1, 10 ** k - 1)
        if n % 10:
            vals.add(g + Fr(n, 10 ** k))
    vals = list(vals)
    srt = sorted(vals)
    ans = " &lt; ".join(dz(v) for v in srt)
    bylen = sorted(vals, key=lambda v: (len(dz(v)), v))
    bynum = sorted(vals, key=lambda v: int(dz(v).split(",")[1]))
    cands = [" &lt; ".join(dz(v) for v in x) for x in (bylen, bynum, list(reversed(srt)), [srt[0], srt[2], srt[1], srt[3]])]
    return mcq("Ordne der Größe nach, beginne mit der kleinsten Zahl: %s" % "; ".join(dz(v) for v in vals), ans, cands,
               "Mit Nullen auf gleich viele Stellen auffüllen und vergleichen: <b>%s</b>." % ans)


def runden():
    v = Fr(R.randint(1, 999)) + Fr(R.randint(1, 999), 1000)
    if (v * 1000) % 10 == 0:
        return None
    k = R.choice([0, 1, 2])
    name = ["auf Ganze", "auf Zehntel (eine Stelle nach dem Komma)", "auf Hundertstel (zwei Stellen nach dem Komma)"][k]
    f = 10 ** k
    r = Fr(int(v * f + Fr(1, 2)), f)
    ab = Fr(int(v * f), f)
    auf = ab + Fr(1, f)
    def show(x):
        s = dz(x)
        if k:
            ip, _, fp = s.partition(",")
            s = ip + "," + fp.ljust(k, "0")
        return s
    wrong = [show(auf if r == ab else ab), dz(v)[:len(dz(v)) - 1] if len(dz(v).split(",")[1]) > k + 1 else show(r + Fr(1, f)), show(r + Fr(1, f)), show(r - Fr(1, f)) if r > Fr(1, f) else None]
    nxt = int(v * f * 10) % 10
    return mcq("Runde %s %s." % (dz(v), name), show(r), wrong,
               "Entscheidend ist die nächste Stelle: %d. %s, also <b>%s</b>." % (nxt, "Bei 0 bis 4 abrunden" if nxt < 5 else "Bei 5 bis 9 aufrunden", show(r)))


def strahl():
    a = R.randint(0, 8)
    step = R.choice([Fr(1, 10), Fr(1, 100)])
    lo = Fr(a) if step == Fr(1, 10) else Fr(a) + Fr(R.randint(0, 9), 10)
    n = 10
    i = R.randint(1, 9)
    v = lo + i * step
    W, x0, y = 430, 28, 50
    u = (W - 56) / 10.0
    s = [line(x0 - 6, y, x0 + 10 * u + 10, y, INK, 2)]
    for j in range(11):
        L = 10 if j in (0, 5, 10) else 6
        s.append(line(x0 + j * u, y - L, x0 + j * u, y + L, INK, 2 if L == 10 else 1.2))
    s.append(text(x0, y + 28, dz(lo), 14) + text(x0 + 10 * u, y + 28, dz(lo + 10 * step), 14))
    s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (x0 + i * u, y - 12, RED) + text(x0 + i * u, y - 27, "A", 15, col=RED))
    pic = wrap(W, y + 40, "".join(s), "Zahlenstrahl mit Dezimalzahlen", lg=True)
    return mcq(pic + "Welche Zahl gehört zum Punkt A?", dz(v), [dz(lo + i * step * 10) if lo + i * step * 10 != v else None, dz(lo + (i + 1) * step), dz(lo + i * step / 10), dz(lo + (10 - i) * step) if i != 5 else None],
               "Ein Strich bedeutet %s. A liegt %d Striche nach %s: <b>%s</b>." % (dz(step), i, dz(lo), dz(v)))


def groessen():
    kind = R.choice(["euro", "m", "kg", "km", "l"])
    if kind == "euro":
        e, c = R.randint(1, 50), R.randint(1, 99)
        return mcq("Schreibe in Euro mit Komma: %d € %d ct" % (e, c), "%d,%02d €" % (e, c),
                   ["%d,%d €" % (e, c) if c < 10 else "%d,%d €" % (e, c // 10), "%s €" % dz(e + Fr(c, 1000)), "%d,%d €" % (e + 1, c) if c >= 10 else "%d,%02d €" % (e, c * 10)],
                   "1 € = 100 ct, also zwei Stellen nach dem Komma: <b>%d,%02d €</b>." % (e, c))
    g, k, f = {"m": ("m", "cm", 100), "kg": ("kg", "g", 1000), "km": ("km", "m", 1000), "l": ("l", "ml", 1000)}[kind]
    a, b = R.randint(1, 20), R.randint(1, f - 1)
    if b % 10 == 0 and f == 1000 and R.random() < 0.5:
        return None
    v = a + Fr(b, f)
    places = len(str(f)) - 1
    ans = "%d,%s %s" % (a, str(b).rjust(places, "0"), g)
    wrong = ["%d,%d %s" % (a, b, g) if len(str(b)) != places else "%d,%s %s" % (a, str(b).rjust(places + 1, "0"), g), "%s %s" % (dz(a + Fr(b, f * 10)), g), "%s %s" % (dz(a + Fr(b, f // 10)), g) if b < f // 10 * 10 and Fr(b, f // 10) < 1 else "%d,%s %s" % (a + 1, str(b).rjust(places, "0"), g)]
    return mcq("Schreibe mit Komma in %s: %d %s %d %s" % (g, a, g, b, k), ans, wrong, "1 %s = %d %s, also %d Stellen nach dem Komma: <b>%s</b>." % (g, f, k, places, ans))


def main():
    seen = set()
    sets = [
        ("Stellenwerte", mix(R, seen, [(stelle, 12), (schreiben, 8)])),
        ("Vergleichen", mix(R, seen, [(vergleich, 20)])),
        ("Ordnen und Zahlenstrahl", mix(R, seen, [(ordnen, 10), (strahl, 10)])),
        ("Runden", mix(R, seen, [(runden, 20)])),
        ("Größen mit Komma", mix(R, seen, [(groessen, 20)])),
    ]
    body = lesson(
        ["Nach dem Komma kommen <b>Zehntel</b>, <b>Hundertstel</b>, <b>Tausendstel</b>: 3,472 = 3 + %s + %s + %s." % (fr(4, 10), fr(7, 100), fr(2, 1000)),
         "Beim <b>Vergleichen</b> vergleicht man Stelle für Stelle von links. Nullen am Ende ändern nichts: 0,5 = 0,50.",
         "<b>Runden</b>: Auf die Stelle danach schauen. Bei 0, 1, 2, 3, 4 abrunden, bei 5, 6, 7, 8, 9 aufrunden.",
         "Bei Größen zeigt das Komma, wo die kleinere Einheit beginnt: 2,05 m = 2 m 5 cm."],
        [example("0,45 ☐ 0,5", ["0,45 und 0,50", "4 Zehntel &lt; 5 Zehntel"], "0,45 &lt; 0,5"),
         example("3,846 auf Zehntel runden", ["Nächste Stelle: 4", "abrunden"], "3,8")],
        [["0,45 &gt; 0,5, weil 45 &gt; 5", "Erst auffüllen: 0,45 &lt; 0,50"],
         ["%s = 0,7" % fr(7, 100), "Hundertstel: 0,07"],
         ["2 m 5 cm = 2,5 m", "2,05 m (5 cm sind 5 Hundertstel Meter)"]])
    faq = [
        {"q": "Wie vergleicht man Dezimalzahlen?", "a": "Erst die Ganzen, dann Stelle für Stelle nach dem Komma. Hilfreich: mit Nullen auf gleich viele Stellen auffüllen."},
        {"q": "Ist 0,5 dasselbe wie 0,50?", "a": "Ja. Nullen am Ende nach dem Komma ändern den Wert nicht."},
        {"q": "Wie rundet man auf Zehntel?", "a": "Man schaut auf die Hundertstel. Ist sie 5 oder mehr, wird aufgerundet, sonst abgerundet."},
        {"q": "Was bedeutet die dritte Stelle nach dem Komma?", "a": "Das sind die Tausendstel. 0,003 = 3/1000."},
    ]
    make_unit(R, "dezimalzahlen-und-stellenwerte", "Z",
              "Die Schülerinnen und Schüler lesen und schreiben Dezimalzahlen, ordnen ihnen Stellenwerte zu, vergleichen, ordnen und runden sie und nutzen die Kommaschreibweise bei Größen (Zusammenfassung).",
              "Dezimalzahlen und Stellenwerte",
              "Dezimalzahlen Klasse 6 – vergleichen, ordnen und runden, Arbeitsblätter",
              "Dezimalzahlen",
              "Dezimalzahlen für Klasse 6: Zehntel, Hundertstel, Tausendstel, vergleichen, ordnen, runden und Größen mit Komma. 100 Aufgaben mit Lösungen, kostenlos.",
              "Nach dem Komma: Zehntel, Hundertstel, Tausendstel.",
              "0,5 = 0,50 – Nullen am Ende ändern nichts.",
              body, faq, sets, 7, grade="klasse-6")


if __name__ == "__main__":
    main()
