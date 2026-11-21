# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Zahlen bis 100（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_zahlen_bis_100.py
Zehner und Einer, Hunderterfeld, Zahlwörter, zerlegen, Nachbarzahlen, bündeln.
Fehler: Zahlendreher (46 ↔ 64), Zehner und Einer vertauscht, Zehnerstangen als Einer gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, wort, stellenwerttafel, dienes, table
from de_k2 import hunderterfeld

R = random.Random(49201)
KIDS = Kids(R)


def dreh(n):
    z, e = divmod(n, 10)
    return e * 10 + z if e and e != z else None


def zehner_einer():
    z, e = R.randint(1, 9), R.randint(0, 9)
    n = 10 * z + e
    return mcq(dienes(0, z, e, "%d Zehnerstangen und %d Einerwürfel" % (z, e)) + "Welche Zahl ist das?", str(n),
               [dreh(n), z + e, n + 10 if n + 10 <= 100 else n - 10, n - 1 if e else n + 1],
               "%d Zehner und %d Einer: %d + %d = <b>%d</b>." % (z, e, 10 * z, e, n))


def feld():
    n = R.randint(11, 99)
    if n % 10 == 0 and R.random() < 0.6:
        return None
    z, e = divmod(n, 10)
    return mcq(hunderterfeld(n) + "Wie viele Punkte sind blau?", str(n), [dreh(n), n + 10 if n + 10 <= 100 else n - 1, n - 10, n + 1],
               "%d volle Zehnerreihen und %d einzelne Punkte: <b>%d</b>." % (z, e, n))


def zahlwort():
    n = R.randint(13, 99)
    z, e = divmod(n, 10)
    if R.random() < 0.5:
        return mcq("Welche Zahl ist „%s“?" % wort(n), str(n), [dreh(n), n + 10, n - 10 if n > 20 else n + 1],
                   "Im Deutschen sagt man zuerst die Einer, dann die Zehner. Man schreibt aber zuerst die Zehner: <b>%d</b>." % n)
    d = dreh(n)
    return mcq("Wie schreibt man die Zahl %d als Wort?" % n, wort(n),
               [wort(d) if d else None, wort(n + 10) if n < 90 else wort(n - 10), wort(n + 1) if e != 9 else wort(n - 1)],
               "%d Zehner, %d Einer: <b>%s</b>." % (z, e, wort(n)))


def zerlegen():
    n = R.randint(21, 99)
    z, e = divmod(n, 10)
    if e == 0:
        return None
    kind = R.choice(["plus", "zehner", "einer", "tafel"])
    if kind == "plus":
        return mcq("%d = ? + %d" % (n, e), str(10 * z), [str(z), str(10 * e), str(n - 1)],
                   "%d hat %d Zehner, das sind %d: %d = <b>%d</b> + %d." % (n, z, 10 * z, n, 10 * z, e))
    if kind == "zehner":
        return mcq("Wie viele Zehner hat die Zahl %d?" % n, str(z), [str(e), str(10 * z), str(n)],
                   "%d = %d Zehner und %d Einer: <b>%d</b> Zehner." % (n, z, e, z))
    if kind == "einer":
        return mcq("Wie viele Einer hat die Zahl %d?" % n, str(e), [str(z), str(10 * e), str(n)],
                   "%d = %d Zehner und %d Einer: <b>%d</b> Einer." % (n, z, e, e))
    return mcq("Welche Zahl steht in der Stellenwerttafel?" + stellenwerttafel(0, z, e).replace("<th>H</th>", "").replace(
        "<td style='text-align:center;min-width:34px'>0</td>", "", 1), str(n), [dreh(n), z + e, n + 10 if n + 10 <= 100 else n - 10],
               "Z steht für Zehner, E für Einer: <b>%d</b>." % n)


def nachbarn():
    kind = R.choice(["vor", "nach", "zehner", "zwischen"])
    n = R.randint(12, 98)
    if kind == "vor":
        return mcq("Welche Zahl kommt direkt <b>vor</b> %d?" % n, str(n - 1), [str(n + 1), str(n - 10), str(dreh(n - 1) or n - 2)],
                   "Der Vorgänger ist um 1 kleiner: <b>%d</b>." % (n - 1))
    if kind == "nach":
        return mcq("Welche Zahl kommt direkt <b>nach</b> %d?" % n, str(n + 1), [str(n - 1), str(n + 10) if n + 10 <= 100 else str(n + 2), str(dreh(n + 1) or n + 2)],
                   "Der Nachfolger ist um 1 größer: <b>%d</b>." % (n + 1))
    if kind == "zehner":
        if n % 10 == 0:
            return None
        lo = n // 10 * 10
        ans = "%d und %d" % (lo, lo + 10)
        return mcq("Zwischen welchen Zehnerzahlen liegt %d?" % n, ans,
                   ["%d und %d" % (lo - 10, lo) if lo >= 10 else "%d und %d" % (lo + 10, lo + 20), "%d und %d" % (n - 1, n + 1), "%d und %d" % (lo + 10, lo + 20) if lo + 20 <= 100 else "%d und %d" % (lo - 20, lo - 10)],
                   "%d liegt zwischen den Nachbarzehnern <b>%s</b>." % (n, ans))
    return mcq("Welche Zahl liegt genau zwischen %d und %d?" % (n - 1, n + 1), str(n), [str(n - 2), str(n + 2), str(dreh(n) or n + 10)],
               "%d, <b>%d</b>, %d." % (n - 1, n, n + 1))


def sache():
    kind = R.choice(["eier", "stifte", "geld", "perlen", "baender"])
    p = KIDS.next()
    z, e = R.randint(2, 9), R.randint(1, 9)
    n = 10 * z + e
    w = [dreh(n), z + e, n + 10 if n + 10 <= 100 else n - 10, n - 1]
    if kind == "eier":
        return mcq("Auf dem Bauernhof liegen %d volle Zehnerpackungen Eier und %d einzelne Eier. Wie viele Eier sind das?" % (z, e), str(n), w,
                   "%d Zehner und %d Einer: <b>%d</b> Eier." % (z, e, n))
    if kind == "stifte":
        return mcq("%s hat %d Stifte. %s packt immer 10 Stifte in eine Schachtel. Wie viele volle Schachteln gibt es?" % (p[0], n, p[1].capitalize()), str(z),
                   [str(e), str(n), str(z + 1)],
                   "%d = %d Zehner und %d Einer: <b>%d</b> volle Schachteln, %d Stifte bleiben übrig." % (n, z, e, z, e))
    if kind == "geld":
        return mcq("%s hat %d Zehn-Euro-Scheine und %d Ein-Euro-Münzen. Wie viel Geld ist das?" % (p[0], z, e), "%d €" % n,
                   ["%d €" % x for x in w if x], "%d · 10 € + %d € = <b>%d €</b>." % (z, e, n))
    if kind == "perlen":
        return mcq("%s fädelt Perlen auf. %s hat %d Ketten mit je 10 Perlen und %d einzelne Perlen. Wie viele Perlen sind das?" % (p[0], p[1].capitalize(), z, e), str(n), w,
                   "%d Zehner und %d Einer: <b>%d</b>." % (z, e, n))
    return mcq("Im Klassenzimmer stehen %d Kisten mit je 10 Büchern. Dazu kommen %d einzelne Bücher. Wie viele Bücher sind es?" % (z, e), str(n), w,
               "%d Zehner und %d Einer: <b>%d</b> Bücher." % (z, e, n))


def main():
    seen = set()
    sets = [
        ("Zehner und Einer", mix(R, seen, [(zehner_einer, 20)])),
        ("Das Hunderterfeld und Zahlwörter", mix(R, seen, [(feld, 10), (zahlwort, 10)])),
        ("Zahlen zerlegen", mix(R, seen, [(zerlegen, 20)])),
        ("Nachbarzahlen und Nachbarzehner", mix(R, seen, [(nachbarn, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Jede Zahl bis 100 hat <b>Zehner</b> und <b>Einer</b>. 10 Einer sind 1 Zehner.",
         "Bei 46 steht die 4 für 4 Zehner (40) und die 6 für 6 Einer.",
         "Wir sprechen zuerst die Einer: sechsundvierzig. Wir schreiben aber zuerst die Zehner: 46.",
         "Der Vorgänger ist 1 kleiner, der Nachfolger ist 1 größer."],
        [example("3 Zehnerstangen und 5 Einerwürfel", ["30 + 5"], "35"),
         example("Nachbarzehner von 67", ["60 < 67 < 70"], "60 und 70")],
        [["sechsundvierzig = 64", "Zehner zuerst schreiben: 46"],
         ["Zehnerstangen wie Einer zählen", "Jede Stange sind 10"],
         ["Der Vorgänger von 40 ist 49", "Der Vorgänger von 40 ist 39"]],
        extra=table(["Zahl", "Zehner", "Einer"], [["46", "4", "6"], ["70", "7", "0"], ["100", "10", "0"]]))
    faq = [
        {"q": "Warum verwechseln Kinder 46 und 64 so oft?", "a": "Weil man im Deutschen zuerst die Einer spricht (sechs-und-vierzig), aber zuerst die Zehner schreibt. Hilfe: beim Schreiben erst die Zehner festlegen."},
        {"q": "Was hilft beim Verstehen der Zahlen bis 100?", "a": "Zehnerstangen und Einerwürfel, das Hunderterfeld und Geld (10-€-Scheine und 1-€-Münzen). So sieht man, dass 10 Einer einen Zehner ergeben."},
        {"q": "Was sind Nachbarzehner?", "a": "Die Zehnerzahlen direkt davor und danach. 67 liegt zwischen den Nachbarzehnern 60 und 70."},
        {"q": "Bis wohin rechnen Kinder in Klasse 2?", "a": "Im Zahlenraum bis 100. In Klasse 3 geht es weiter bis 1000."},
    ]
    make_unit(R, "zahlen-bis-100", "Z",
              "Die Schülerinnen und Schüler verstehen den Aufbau der Zahlen bis 100 aus Zehnern und Einern, stellen Zahlen mit Material und im Hunderterfeld dar, lesen und schreiben Zahlwörter und bestimmen Nachbarzahlen (Zusammenfassung).",
              "Zahlen bis 100: Zehner und Einer",
              "Zahlen bis 100 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Zahlen bis 100",
              "Zahlen bis 100 für Klasse 2: Zehner und Einer, Hunderterfeld, Zahlwörter, Zahlen zerlegen und Nachbarzahlen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "46 = 4 Zehner und 6 Einer.",
              "Zuerst die Zehner schreiben, dann die Einer.",
              body, faq, sets, 1, grade="klasse-2")


if __name__ == "__main__":
    main()
