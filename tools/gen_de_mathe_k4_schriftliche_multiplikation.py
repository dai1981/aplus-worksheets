# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Schriftliche Multiplikation（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k4_schriftliche_multiplikation.py
Mal einstellige Zahl, mal Zehnerzahl, mal zweistellige Zahl (Teilprodukte), Überschlag, Sachaufgaben.
Fehler: Übertrag vergessen, Null beim Zehnerteilprodukt vergessen (345 · 27 → 345 · 2 + 345 · 7 = 3105), nur ein Teilprodukt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, wrap
from ws_common import line, text, INK, GREEN

R = random.Random(49104)
KIDS = Kids(R)


def mal_svg(a, b, rows=3):
    """Malaufgabe auf Karopapier: a · b, darunter leere Zeilen"""
    c = 24
    t = "%d%s%d" % (a, MAL, b)
    W = len(t) + 3
    H = rows + 2
    s = []
    for i in range(W + 1):
        s.append(line(4 + i * c, 4, 4 + i * c, 4 + H * c, "#bcd6e6", 1))
    for j in range(H + 1):
        s.append(line(4, 4 + j * c, 4 + W * c, 4 + j * c, "#bcd6e6", 1))
    for k, ch in enumerate(t):
        s.append(text(4 + (k + 1) * c + c / 2, 4 + c * 0.75, ch, 17, col=GREEN if ch == MAL else INK))
    s.append(line(4 + c, 4 + c + 2, 4 + (W - 1) * c, 4 + c + 2, INK, 2))
    s.append(line(4 + c, 4 + (H - 1) * c, 4 + (W - 1) * c, 4 + (H - 1) * c, INK, 2))
    return wrap(W * c + 8, H * c + 8, "".join(s), "schriftliche Multiplikation")


def nocarry(a, d):
    return int("".join(str(int(x) * d % 10) for x in str(a)))


def einstellig():
    a = R.randint(112, 9876)
    d = R.randint(3, 9)
    r = a * d
    if r >= 1000000:
        return None
    w = [nocarry(a, d), r + d, r - 10, a * (d + 1), r + 100]
    return mcq(mal_svg(a, d, 1) + "Rechne schriftlich: %s %s %d" % (num(a), MAL, d), num(r), [num(x) for x in w if x > 0 and x != r],
               "Von rechts: jede Ziffer mal %d, Überträge zur nächsten Stelle dazu. Ergebnis: <b>%s</b>." % (d, num(r)))


def zehner():
    a = R.randint(112, 9876)
    z = R.randint(2, 9) * 10
    if R.random() < 0.3:
        z *= 10
    r = a * z
    if r >= 1000000:
        return None
    w = [a * (z // 10) if z < 100 else a * (z // 100), r * 10 if r * 10 < 10 ** 6 else r + 1000, r + z, a * (z // 10) + 10 if z < 100 else r + 100]
    return mcq("%s %s %s = ?" % (num(a), MAL, num(z)), num(r), [num(x) for x in w if x and x > 0 and x != r],
               "Rechne %s %s %d = %s und hänge %s an: <b>%s</b>." % (num(a), MAL, z // (10 if z < 100 else 100), num(a * (z // (10 if z < 100 else 100))),
                                                                     "eine Null" if z < 100 else "zwei Nullen", num(r)))


def zweistellig():
    a = R.randint(112, 4999)
    b = R.randint(12, 89)
    if b % 10 == 0 or a * b >= 1000000:
        return None
    z, e = b // 10, b % 10
    p1, p2 = a * z * 10, a * e
    r = p1 + p2
    w = [a * z + p2, p1, p2 + p1 + 1000, a * (z + e)]
    return mcq(mal_svg(a, b) + "Rechne schriftlich: %s %s %d" % (num(a), MAL, b), num(r), [num(x) for x in w if x > 0 and x != r],
               "Teilprodukte: %s %s %d = %s und %s %s %d = %s. Zusammen <b>%s</b>." % (num(a), MAL, z * 10, num(p1), num(a), MAL, e, num(p2), num(r)))


def teilprodukte():
    a = R.randint(112, 999)
    b = R.randint(12, 89)
    if b % 10 == 0:
        return None
    z, e = b // 10, b % 10
    ans = "%s und %s" % (num(a * z * 10), num(a * e))
    w = ["%s und %s" % (num(a * z), num(a * e)), "%s und %s" % (num(a * z * 10), num(a * e * 10)), "%s und %s" % (num(a * e), num(a * z))]
    return mcq("Welche Teilprodukte gehören zu %s %s %d?" % (num(a), MAL, b), ans, w,
               "%d = %d + %d. %s %s %d = %s und %s %s %d = %s." % (b, z * 10, e, num(a), MAL, z * 10, num(a * z * 10), num(a), MAL, e, num(a * e)))


def ueberschlag():
    a = R.randint(120, 980)
    b = R.randint(12, 89)
    ra = (a + 50) // 100 * 100
    rb = (b + 5) // 10 * 10
    est = ra * rb
    exact = a * b
    claim = R.choice([exact, exact, exact * 10, exact + 10000])
    q = "Lena rechnet %s %s %d = %s. Überschlage: Kann das stimmen?" % (num(a), MAL, b, num(claim))
    ok = claim == exact
    ans = "%s, der Überschlag ist etwa %s." % ("Ja" if ok else "Nein", num(est))
    w = ["%s, der Überschlag ist etwa %s." % ("Nein" if ok else "Ja", num(est)), "Ja, der Überschlag ist etwa %s." % num(est * 10),
         "Nein, der Überschlag ist etwa %s." % num(est // 10)]
    return mcq(q, ans, w, "%s %s %d ≈ %s %s %d = %s. %s" % (num(a), MAL, b, num(ra), MAL, rb, num(est), "Das Ergebnis passt." if ok else "%s ist viel zu weit weg." % num(claim)))


def sache():
    kind = R.choice(["kiste", "eintritt", "jahr", "seiten", "flug"])
    p = KIDS.next()
    if kind == "kiste":
        a, b = R.randint(24, 48), R.randint(112, 960)
        q = "In einer Kiste sind %d Flaschen. Ein Lastwagen bringt %s Kisten. Wie viele Flaschen sind das?" % (a, num(b))
        r, u = a * b, "Flaschen"
    elif kind == "eintritt":
        a, b = R.randint(12, 29), R.randint(240, 980)
        q = "Eine Eintrittskarte für das Musical kostet %d €. Es werden %s Karten verkauft. Wie viel Geld wird eingenommen?" % (a, num(b))
        r, u = a * b, "€"
    elif kind == "jahr":
        a = R.randint(12, 48)
        q = "Ein Bäcker backt jeden Tag %d Bleche mit je 24 Brötchen. Wie viele Brötchen sind das in 365 Tagen?" % a
        r, u = a * 24 * 365, "Brötchen"
        if r >= 1000000:
            return None
        return mcq(q, "%s %s" % (num(r), u), ["%s %s" % (num(x), u) for x in (a * 24 + 365, a * 24 * 36, r + 1000) if x != r],
                   "Pro Tag: %d %s 24 = %s. Im Jahr: %s %s 365 = <b>%s</b>." % (a, MAL, num(a * 24), num(a * 24), MAL, num(r)))
    elif kind == "seiten":
        a, b = R.randint(120, 480), R.randint(25, 86)
        q = "Eine Druckerei druckt %d Bücher mit je %s Seiten. Wie viele Seiten sind das?" % (b, num(a))
        r, u = a * b, "Seiten"
    else:
        a, b = R.randint(160, 380), R.randint(12, 52)
        q = "Ein Flugzeug hat %s Sitzplätze und fliegt in einem Monat %d-mal ausgebucht. Wie viele Fluggäste sind das?" % (num(a), b)
        r, u = a * b, "Fluggäste"
    if r >= 1000000:
        return None
    w = [a * (b // 10) + a * (b % 10) if b >= 10 else r + a, r + 1000, r - a, a + b]
    return mcq(q, "%s %s" % (num(r), u), ["%s %s" % (num(x), u) for x in w if x > 0 and x != r],
               "%s %s %s = <b>%s %s</b>." % (num(a), MAL, num(b), num(r), u))


def main():
    seen = set()
    sets = [
        ("Mal einstellige Zahlen", mix(R, seen, [(einstellig, 20)])),
        ("Mal Zehner- und Hunderterzahlen", mix(R, seen, [(zehner, 20)])),
        ("Mal zweistellige Zahlen", mix(R, seen, [(zweistellig, 20)])),
        ("Teilprodukte und Überschlag", mix(R, seen, [(teilprodukte, 12), (ueberschlag, 8)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Bei der schriftlichen Multiplikation mit einer einstelligen Zahl nimmst du jede Ziffer von rechts nach links mal und schreibst Überträge in die nächste Stelle.",
         "Bei einer zweistelligen Zahl rechnest du zwei <b>Teilprodukte</b>: erst mit den Zehnern, dann mit den Einern.",
         "Das Teilprodukt mit den Zehnern rückt eine Stelle nach links (oder du schreibst eine 0 dazu).",
         "Zum Schluss addierst du die Teilprodukte. Ein Überschlag zeigt, ob das Ergebnis passt."],
        [example("345 %s 27" % MAL, ["345 %s 20 = 6900" % MAL, "345 %s 7 = 2415" % MAL, "6900 + 2415 = 9315"], "9315"),
         example("1234 %s 6" % MAL, ["4 %s 6 = 24 → 4, Übertrag 2" % MAL, "3 %s 6 + 2 = 20 → 0, Übertrag 2" % MAL, "2 %s 6 + 2 = 14 → 4, Übertrag 1" % MAL, "1 %s 6 + 1 = 7" % MAL], "7404")],
        [["345 %s 27 = 690 + 2415 = 3105" % MAL, "Das Zehnerteilprodukt ist 6900, nicht 690"],
         ["Übertrag vergessen", "Übertrag zur nächsten Stelle addieren"],
         ["Nur 345 %s 7 rechnen" % MAL, "Beide Teilprodukte addieren"]])
    faq = [
        {"q": "Wann lernen Kinder die schriftliche Multiplikation?", "a": "In den meisten Bundesländern in Klasse 4, zuerst mit einstelligen, dann mit zweistelligen Zahlen."},
        {"q": "Warum rückt man beim zweiten Teilprodukt ein?", "a": "Weil man mit Zehnern multipliziert: 345 · 2 Zehner = 690 Zehner = 6900."},
        {"q": "Muss man die Malaufgabe vertauschen?", "a": "Nein, aber es ist oft leichter, die Zahl mit weniger Stellen nach rechts zu schreiben."},
        {"q": "Wie prüft man das Ergebnis?", "a": "Mit einem Überschlag: 345 · 27 ≈ 300 · 30 = 9000. Das Ergebnis 9315 passt."},
    ]
    make_unit(R, "schriftliche-multiplikation", "Z",
              "Die Schülerinnen und Schüler multiplizieren schriftlich mit ein- und zweistelligen Zahlen, verstehen die Teilprodukte und kontrollieren mit Überschlägen (Zusammenfassung).",
              "Schriftliche Multiplikation mit Teilprodukten",
              "Schriftliche Multiplikation Klasse 4 – Arbeitsblätter mit Lösungen",
              "Schriftliche Multiplikation",
              "Schriftliche Multiplikation für Klasse 4: mal einstellige, mal Zehnerzahlen und mal zweistellige Zahlen, Teilprodukte, Überschlag und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Erst die Zehner, dann die Einer, dann addieren.",
              "345 · 27 = 6900 + 2415 = 9315",
              body, faq, sets, 4, grade="klasse-4")


if __name__ == "__main__":
    main()
