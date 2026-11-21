# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Schriftliche Division durch einstellige Zahlen（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k4_schriftliche_division.py
Ohne Rest, mit Null im Ergebnis, mit Rest, Probe und Überschlag, Sachaufgaben.
Fehler: Null im Ergebnis vergessen (4824 : 4 → 126), Rest größer als der Teiler, erste Stelle falsch gewählt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, wrap
from ws_common import line, text, INK, GREEN

R = random.Random(49105)
KIDS = Kids(R)


def div_svg(a, d):
    c = 24
    t = "%d%s%d=" % (a, GETEILT, d)
    W = len(t) + 5
    H = 5
    s = []
    for i in range(W + 1):
        s.append(line(4 + i * c, 4, 4 + i * c, 4 + H * c, "#bcd6e6", 1))
    for j in range(H + 1):
        s.append(line(4, 4 + j * c, 4 + W * c, 4 + j * c, "#bcd6e6", 1))
    for k, ch in enumerate(t):
        s.append(text(4 + (k + 1) * c + c / 2, 4 + c * 0.75, ch, 17, col=GREEN if ch in (GETEILT, "=") else INK))
    return wrap(W * c + 8, H * c + 8, "".join(s), "schriftliche Division")


def rr(q, r):
    return "%s Rest %d" % (num(q), r) if r else num(q)


def drop0(q):
    s = str(q)
    t = s[0] + s[1:].replace("0", "")
    return int(t) if t != s else None


def task(kind):
    def mk():
        d = R.randint(2, 9)
        q = R.randint(102, 1999 if kind != "rest" else 999)
        if kind == "null" and "0" not in str(q)[1:]:
            return None
        if kind == "ohne" and "0" in str(q)[1:]:
            return None
        r = R.randint(1, d - 1) if kind == "rest" else 0
        a = q * d + r
        if a > 9999:
            return None
        w = [rr(drop0(q), r) if drop0(q) else None, rr(q + 1, r), rr(q - 1, r + d) if r else rr(q - 1, 0), rr(q, (r + 1) % d) if r else rr(q * 10, 0),
             rr(q + 10, r)]
        return mcq(div_svg(a, d) + "Rechne schriftlich: %s %s %d" % (num(a), GETEILT, d), rr(q, r), [x for x in w if x and x != rr(q, r)],
                   "Teile Stelle für Stelle von links. %sErgebnis: <b>%s</b>. Probe: %s %s %d%s = %s."
                   % ("Passt der Teiler nicht hinein, schreibst du eine 0 ins Ergebnis. " if "0" in str(q)[1:] else "", rr(q, r), num(q), MAL, d,
                      " + %d" % r if r else "", num(a)))
    return mk


def probe():
    d = R.randint(3, 9)
    q = R.randint(120, 999)
    r = R.randint(1, d - 1)
    a = q * d + r
    ans = "%s %s %d + %d = %s" % (num(q), MAL, d, r, num(a))
    w = ["%s %s %d − %d = %s" % (num(q), MAL, d, r, num(q * d - r)), "%s %s %d = %s" % (num(q), MAL, d, num(q * d)),
         "%s %s %d + %d = %s" % (num(q), MAL, r, d, num(q * r + d))]
    return mcq("Welche Probe passt zu %s %s %d = %s Rest %d?" % (num(a), GETEILT, d, num(q), r), ans, w,
               "Ergebnis mal Teiler plus Rest: <b>%s</b>." % ans)


def ueberschlag():
    d = R.randint(3, 9)
    q = R.randint(110, 1100)
    a = q * d
    if a > 9999:
        return None
    est_a = None
    for cand in (a // 100 * 100, (a // 100 + 1) * 100, a // 1000 * 1000, (a // 1000 + 1) * 1000):
        if cand % d == 0 and cand > 0:
            est_a = cand
            break
    if not est_a:
        return None
    est = est_a // d
    w = [est * 10, est // 10 if est >= 10 else est + 100, est + 100 if est + 100 != est * 10 else est + 200]
    return mcq("Überschlage: %s %s %d ≈ ?" % (num(a), GETEILT, d), "etwa %s" % num(est), ["etwa %s" % num(x) for x in w if x != est and x > 0],
               "Suche eine passende Zahl in der Nähe: %s %s %d = %s. Also etwa <b>%s</b>. (Genau: %s)" % (num(est_a), GETEILT, d, num(est), num(est), num(q)))


def sache():
    kind = R.choice(["teilen", "preis", "bus", "rest"])
    d = R.randint(3, 9)
    if kind == "teilen":
        q = R.randint(105, 999)
        a = q * d
        txt = "Ein Lottogewinn von %s € wird gerecht unter %d Freunden aufgeteilt. Wie viel bekommt jeder?" % (num(a), d)
        return mcq(txt, "%s €" % num(q), ["%s €" % num(x) for x in (drop0(q) or q + 10, q + 1, q * 10, a - d) if x != q],
                   "%s %s %d = <b>%s €</b>." % (num(a), GETEILT, d, num(q)))
    if kind == "preis":
        q = R.randint(12, 120)
        a = q * d
        txt = "%d gleiche Fahrräder kosten zusammen %s €. Wie viel kostet ein Fahrrad?" % (d, num(a))
        return mcq(txt, "%s €" % num(q), ["%s €" % num(x) for x in (q + 1, q * 10, a - d, q - 1) if x != q],
                   "%s %s %d = <b>%s €</b>." % (num(a), GETEILT, d, num(q)))
    if kind == "bus":
        cap = R.choice([8, 9])
        q = R.randint(10, 60)
        r = R.randint(1, cap - 1)
        a = q * cap + r
        txt = "%s Kinder fahren mit Kleinbussen zum Sportfest der Schulen. In jeden Bus passen %d Kinder. Wie viele Busse braucht man?" % (num(a), cap)
        return mcq(txt, "%d Busse" % (q + 1), ["%d Busse" % x for x in (q, q + 2, q - 1)],
                   "%s %s %d = %d Rest %d. Für die restlichen %d Kinder braucht man noch einen Bus: <b>%d Busse</b>." % (num(a), GETEILT, cap, q, r, r, q + 1))
    q = R.randint(50, 400)
    r = R.randint(1, d - 1)
    a = q * d + r
    txt = "Eine Gärtnerei pflanzt %s Blumen in Reihen zu je %d. Wie viele volle Reihen gibt es, und wie viele Blumen bleiben übrig?" % (num(a), d)
    ans = "%d volle Reihen, %s übrig" % (q, "1 Blume" if r == 1 else "%d Blumen" % r)
    w = ["%d volle Reihen, %s übrig" % (q + 1, "1 Blume" if r == 1 else "%d Blumen" % r), "%d volle Reihen, %d Blumen übrig" % (q, r + d),
         "%d volle Reihen, keine übrig" % q]
    return mcq(txt, ans, w, "%s %s %d = %d Rest %d: <b>%s</b>." % (num(a), GETEILT, d, q, r, ans))


def main():
    seen = set()
    sets = [
        ("Ohne Rest", mix(R, seen, [(task("ohne"), 20)])),
        ("Mit Null im Ergebnis", mix(R, seen, [(task("null"), 20)])),
        ("Mit Rest", mix(R, seen, [(task("rest"), 20)])),
        ("Probe und Überschlag", mix(R, seen, [(probe, 10), (ueberschlag, 10)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Bei der schriftlichen Division teilst du <b>von links nach rechts</b>, Stelle für Stelle.",
         "Ist die erste Ziffer kleiner als der Teiler, nimmst du die ersten zwei Ziffern zusammen.",
         "Nach jedem Schritt: mal rechnen, abziehen, die nächste Ziffer herunterholen.",
         "Passt der Teiler nicht hinein, schreibst du eine <b>0</b> ins Ergebnis. Am Ende bleibt manchmal ein Rest."],
        [example("4824 %s 4" % GETEILT, ["4 : 4 = 1", "8 : 4 = 2", "2 : 4 = 0, Rest 2 → 24", "24 : 4 = 6"], "1206"),
         example("957 %s 6" % GETEILT, ["9 : 6 = 1, Rest 3 → 35", "35 : 6 = 5, Rest 5 → 57", "57 : 6 = 9, Rest 3"], "159 Rest 3")],
        [["4824 %s 4 = 126" % GETEILT, "Die 0 nicht vergessen: 1206"],
         ["Rest größer als der Teiler", "Der Rest muss kleiner als der Teiler sein"],
         ["Von rechts anfangen", "Bei der Division immer links beginnen"]])
    faq = [
        {"q": "Wann lernen Kinder die schriftliche Division?", "a": "In Klasse 4, meist durch einstellige Zahlen. Die Division durch zweistellige Zahlen folgt oft erst in Klasse 5."},
        {"q": "Warum ist die Null im Ergebnis so wichtig?", "a": "Sie hält eine Stelle frei. Ohne sie wäre das Ergebnis zehnmal zu klein, zum Beispiel 126 statt 1206."},
        {"q": "Wie macht man die Probe?", "a": "Ergebnis mal Teiler, dann den Rest addieren. Es muss die Ausgangszahl herauskommen."},
        {"q": "Was tun, wenn die erste Ziffer kleiner als der Teiler ist?", "a": "Dann nimmt man die ersten beiden Ziffern zusammen, zum Beispiel bei 2496 : 4 zuerst 24 : 4."},
    ]
    make_unit(R, "schriftliche-division", "Z",
              "Die Schülerinnen und Schüler dividieren schriftlich durch einstellige Zahlen, auch mit Rest und mit Nullen im Ergebnis, und kontrollieren mit Probe und Überschlag (Zusammenfassung).",
              "Schriftliche Division durch einstellige Zahlen",
              "Schriftliche Division Klasse 4 – Arbeitsblätter mit Lösungen",
              "Schriftliche Division",
              "Schriftliche Division für Klasse 4: durch einstellige Zahlen, mit Null im Ergebnis, mit Rest, Probe, Überschlag und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Von links teilen: mal, minus, herunterholen.",
              "Passt der Teiler nicht hinein, kommt eine 0 ins Ergebnis.",
              body, faq, sets, 5, grade="klasse-4")


if __name__ == "__main__":
    main()
