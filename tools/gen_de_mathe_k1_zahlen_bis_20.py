# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Zahlen bis 20（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_zahlen_bis_20.py
Zwanzigerfeld, Zehner und Einer, Zahlwörter elf bis zwanzig, Zahlenstrahl bis 20, Nachbarzahlen.
Fehler: Zahlendreher (14 ↔ 41), den vollen Zehner einzeln gezählt und verzählt, am Zahlenstrahl falsch gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, dienes, wort
from de_k2 import de, zahlenstrahl100
from k_pics import tenframe_svg

R = random.Random(49402)


def nah(n, lo=0, hi=20):
    return [str(x) for x in (n + 1, n - 1, n + 2, n - 2, n + 10, n - 10) if lo <= x <= hi and x != n]


def feld():
    n = R.randint(11, 20)
    pic = de(tenframe_svg(n, 2), "Zwanzigerfeld mit %d Punkten" % n)
    return mcq(pic + "Wie viele Punkte sind es?", str(n), nah(n, 5),
               "Ein volles Zehnerfeld sind 10. Dazu %d: 10 + %d = <b>%d</b>." % (n - 10, n - 10, n))


def ze():
    n = R.randint(11, 20)
    z, e = divmod(n, 10)
    kind = R.choice(["bild", "plus", "teil", "text", "minus"])
    if kind == "text":
        if n == 20:
            return None
        return mcq("1 Zehner und %d Einer. Welche Zahl ist das?" % e, str(n), [str(10 * e + 1) if e > 1 else "12", str(1 + e), str(n + 1)],
                   "10 + %d = <b>%d</b>." % (e, n))
    if kind == "minus":
        if n == 20:
            return None
        return mcq("%d − %d = ?" % (n, e), "10", [str(e), "1", str(n - e - 1)],
                   "Nimmst du die %d Einer weg, bleibt der Zehner: <b>10</b>." % e)
    if kind == "bild":
        return mcq(dienes(0, z, e, "%d Zehnerstange%s und %d Einerwürfel" % (z, "n" if z > 1 else "", e)) + "Welche Zahl ist das?", str(n),
                   [str(10 * e + z) if e else "2", str(z + e), str(n + 1)],
                   "1 Zehner und %d Einer: <b>%d</b>." % (e, n) if z == 1 else "2 Zehner: <b>20</b>.")
    if kind == "plus":
        if n == 20:
            return None
        return mcq("10 + %d = ?" % e, str(n), [str(10 * e + 1) if e > 1 else "11", str(n + 1), str(e)],
                   "Ein Zehner und %d Einer: <b>%d</b>." % (e, n))
    if n == 20:
        return None
    return mcq("Wie viele Einer hat die Zahl %d?" % n, str(e), ["1", str(n), str(e + 1)] if e != 1 else ["10", str(n), "2"],
               "%d = 1 Zehner und <b>%d</b> Einer." % (n, e))


def woerter():
    n = R.randint(11, 20)
    if R.random() < 0.5:
        d = 10 * (n % 10) + 1 if n < 20 else 2
        return mcq("Welche Zahl ist „%s“?" % wort(n), str(n), [str(d) if d != n else "12", str(n + 1) if n < 20 else "19", str(n - 1)],
                   "„%s“: zuerst hört man die Einer, aber man schreibt zuerst die 1 für den Zehner: <b>%d</b>." % (wort(n).capitalize(), n) if 13 <= n <= 19 else
                   "„%s“ ist die <b>%d</b>." % (wort(n).capitalize(), n))
    w = [wort(n + 1) if n < 20 else wort(18), wort(n - 1), wort(n % 10) if n % 10 else wort(10), wort(n + 2) if n < 19 else wort(17)]
    return mcq("Wie heißt die Zahl %d als Wort?" % n, wort(n), [x for x in dict.fromkeys(w) if x != wort(n)], "%d heißt <b>%s</b>." % (n, wort(n)))


def strahl():
    v = R.randint(1, 19)
    if v in (5, 10, 15):
        return None
    if R.random() < 0.5:
        u = R.choice([x for x in range(1, 20) if x not in (5, 10, 15, v)])
        ch = R.choice("AB")
        marks = [(v, ch), (u, "B" if ch == "A" else "A")]
        pic = zahlenstrahl100(0, 20, sorted(marks), step=1, every=5, width=440)
        return mcq(pic + "Welche Zahl zeigt der Pfeil %s?" % ch, str(v), [str(u)] + nah(v, 0),
                   "Zähle die Striche von %d aus: <b>%d</b>." % (v // 5 * 5, v))
    pic = zahlenstrahl100(0, 20, [(v, "A")], step=1, every=5, width=440)
    return mcq(pic + "Welche Zahl zeigt der Pfeil?", str(v), nah(v, 0),
               "Zähle die Striche von %d aus: <b>%d</b>." % (v // 5 * 5, v))


def nachbar():
    kind = R.choice(["vor", "nach", "zwischen", "fehlt", "groesser"])
    n = R.randint(11, 19)
    if kind == "vor":
        return mcq("Welche Zahl kommt direkt vor der %d?" % n, str(n - 1), [str(n + 1), str(n - 2), str(n - 10)], "Eins weniger: <b>%d</b>." % (n - 1))
    if kind == "nach":
        return mcq("Welche Zahl kommt direkt nach der %d?" % n, str(n + 1), [str(n - 1), str(n + 2), str(n - 9)], "Eins mehr: <b>%d</b>." % (n + 1))
    if kind == "zwischen":
        return mcq("Welche Zahl liegt zwischen %d und %d?" % (n - 1, n + 1), str(n), [str(n - 2), str(n + 2), str(n + 10) if n + 10 <= 20 else str(n - 10)],
                   "%d, <b>%d</b>, %d." % (n - 1, n, n + 1))
    if kind == "fehlt":
        s = R.randint(10, 16)
        k = R.randint(1, 3)
        seq = [str(s + i) if i != k else "?" for i in range(5)]
        return mcq("Welche Zahl fehlt? %s" % ", ".join(seq), str(s + k), [str(s + k + 1), str(s + k - 1), str(s + k + 2)], "Immer 1 weiter: <b>%d</b>." % (s + k))
    a, b = R.sample(range(10, 21), 2)
    big = max(a, b)
    return mcq("Welche Zahl ist größer: %d oder %d?" % (a, b), str(big), [str(min(a, b)), "Beide sind gleich groß", "Das kann man nicht sagen"],
               "Die %d kommt in der Zahlenreihe später: <b>%d</b> ist größer." % (big, big))


def main():
    seen = set()
    sets = [
        ("Im Zwanzigerfeld", mix(R, seen, [(feld, 10), (ze, 10)])),
        ("Zehner und Einer", mix(R, seen, [(ze, 20)])),
        ("Zahlwörter bis 20", mix(R, seen, [(woerter, 20)])),
        ("Am Zahlenstrahl", mix(R, seen, [(strahl, 20)])),
        ("Nachbarzahlen", mix(R, seen, [(nachbar, 20)])),
    ]
    body = lesson(
        ["Die Zahlen von 11 bis 19 haben <b>1 Zehner</b> und noch Einer dazu.",
         "14 heißt: 1 Zehner und 4 Einer. Man spricht „vierzehn“, schreibt aber zuerst die 1.",
         "20 sind 2 Zehner.",
         "Am Zahlenstrahl liegen kleine Zahlen links, große Zahlen rechts."],
        [example("Ein volles Zehnerfeld und 6 Punkte", ["10 + 6"], "16"),
         example("siebzehn", ["1 Zehner, 7 Einer"], "17")],
        [["vierzehn = 41", "vierzehn = 14"],
         ["Beim Zwanzigerfeld alles einzeln zählen und sich verzählen", "Volles Zehnerfeld = 10, dann weiterzählen"],
         ["Am Zahlenstrahl bei 1 anfangen", "Der erste Strich ist die 0"]])
    faq = [
        {"q": "Warum verwechseln Kinder 14 und 41?", "a": "Weil man „vier-zehn“ sagt, also die Einer zuerst hört. Hilfe: erst die 1 für den Zehner schreiben, dann die Einer."},
        {"q": "Was ist ein Zwanzigerfeld?", "a": "Zwei Zehnerfelder nebeneinander. Ein volles Feld sind 10, so erkennt man Zahlen bis 20 schnell."},
        {"q": "Wie lernen Kinder die Zahlen bis 20?", "a": "Mit Zehnerstangen, Rechenketten, dem Zwanzigerfeld und dem Zahlenstrahl."},
        {"q": "Was sind Nachbarzahlen?", "a": "Die Zahl direkt davor und direkt danach. Die Nachbarn der 15 sind 14 und 16."},
    ]
    make_unit(R, "zahlen-bis-20", "Z",
              "Die Schülerinnen und Schüler stellen Zahlen bis 20 im Zwanzigerfeld und mit Zehnern und Einern dar, lesen und schreiben Zahlwörter, orientieren sich am Zahlenstrahl und bestimmen Nachbarzahlen (Zusammenfassung).",
              "Zahlen bis 20",
              "Zahlen bis 20 Klasse 1 – Arbeitsblätter mit Lösungen",
              "Zahlen bis 20",
              "Zahlen bis 20 für Klasse 1: Zwanzigerfeld, Zehner und Einer, Zahlwörter, Zahlenstrahl und Nachbarzahlen. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "14 = 1 Zehner und 4 Einer",
              "Erst die 1 schreiben, dann die Einer.",
              body, faq, sets, 2, grade="klasse-1")


if __name__ == "__main__":
    main()
