# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Verdoppeln und halbieren（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_verdoppeln_und_halbieren.py
Verdoppeln mit Bildern, Verdopplungsaufgaben bis 20, halbieren, Fast-Verdopplungen (6 + 7), Sachaufgaben.
Fehler: beim Verdoppeln nur 1 dazu (Doppelte von 6 = 7), beim Halbieren verdoppelt, bei 6 + 7 die Verdopplung ohne +1.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, table
from de_k2 import de, KINDS, DING, ding
from k_pics import two_groups_svg, row_svg

R = random.Random(49409)
KIDS = Kids(R)


def bild():
    n = R.randint(1, 9)
    k = R.choice(KINDS)
    pic = de(two_groups_svg(n, k, n, k, word="|"), "zweimal %s" % ding(k, n))
    return mcq(pic + "Hier sind zweimal %s. Wie viele sind es zusammen?" % ding(k, n), str(2 * n), [str(n + 1), str(2 * n + 1), str(2 * n - 1)],
               "Das Doppelte von %d: %d + %d = <b>%d</b>." % (n, n, n, 2 * n))


def dopp():
    n = R.randint(1, 10)
    kind = R.choice(["plus", "wort", "luecke"])
    if kind == "plus":
        return mcq("%d + %d = ?" % (n, n), str(2 * n), [str(n + 1), str(2 * n + 1), str(2 * n - 2) if n > 1 else "4"], "%d + %d = <b>%d</b>." % (n, n, 2 * n))
    if kind == "wort":
        return mcq("Verdopple %d." % n, str(2 * n), [str(n + 1) if n + 1 != 2 * n else "3", str(n // 2) if n % 2 == 0 and n > 2 else str(2 * n + 2), str(2 * n - 1)], "%d + %d = <b>%d</b>." % (n, n, 2 * n))
    return mcq("? + ? = %d (zweimal dieselbe Zahl)" % (2 * n), str(n), [str(2 * n), str(n + 1), str(n - 1) if n > 1 else "2"], "<b>%d</b> + %d = %d." % (n, n, 2 * n))


def halb():
    n = R.randint(1, 10)
    k = R.choice(KINDS)
    if R.random() < 0.5:
        pic = de(row_svg(2 * n, k, per_row=10), ding(k, 2 * n))
        return mcq(pic + "Zwei Kinder teilen gerecht. Wie viele %s bekommt jedes Kind?" % DING[k][1], str(n), [str(2 * n), str(n + 1), str(n - 1) if n > 1 else "3"],
                   "Die Hälfte von %d ist <b>%d</b>, denn %d + %d = %d." % (2 * n, n, n, n, 2 * n))
    return mcq("Halbiere %d." % (2 * n), str(n), [str(4 * n) if 4 * n <= 40 else str(n + 2), str(n + 1), str(2 * n - 1)],
               "%d + %d = %d. Die Hälfte von %d ist <b>%d</b>." % (n, n, 2 * n, 2 * n, n))


def fast():
    n = R.randint(2, 9)
    if R.random() < 0.3:
        return mcq("%d + %d = ?" % (n + 1, n), str(2 * n + 1), [str(2 * n), str(2 * n + 2), str(2 * n + 3)],
                   "%d + %d = %d, und 1 mehr: <b>%d</b>." % (n, n, 2 * n, 2 * n + 1))
    if R.random() < 0.5:
        return mcq("%d + %d = ?" % (n, n + 1), str(2 * n + 1), [str(2 * n), str(2 * n + 2), str(2 * n - 1)],
                   "Verdoppeln und 1 dazu: %d + %d = %d, also <b>%d</b>." % (n, n, 2 * n, 2 * n + 1))
    return mcq("Du weißt: %d + %d = %d. Wie viel ist %d + %d?" % (n, n, 2 * n, n, n - 1), str(2 * n - 1), [str(2 * n), str(2 * n + 1), str(2 * n - 2)],
               "1 weniger als %d: <b>%d</b>." % (2 * n, 2 * n - 1))


def sache():
    kind = R.choice(["socken", "zwillinge", "teilen", "fuesse", "kuchen", "verdoppelt"])
    p = KIDS.next()
    n = R.randint(2, 9)
    if kind == "socken":
        return mcq("Im Schrank liegen %d Paar Socken. Wie viele Socken sind das?" % n, str(2 * n), [str(n), str(n + 2), str(2 * n + 1)],
                   "Ein Paar sind 2 Socken: %d + %d = <b>%d</b>." % (n, n, 2 * n))
    if kind == "zwillinge":
        return mcq("Die Zwillinge Mia und Ben haben jeder %d Murmeln. Wie viele Murmeln haben sie zusammen?" % n, str(2 * n), [str(n), str(n + 2), str(2 * n - 1)],
                   "Das Doppelte von %d: <b>%d</b>." % (n, 2 * n))
    if kind == "teilen":
        return mcq("%s und die Freundin teilen %d Erdbeeren gerecht. Wie viele bekommt jede?" % (p[0], 2 * n) if p[1] == "sie" else
                   "%s und sein Freund teilen %d Erdbeeren gerecht. Wie viele bekommt jeder?" % (p[0], 2 * n), str(n), [str(2 * n), str(n + 1), str(n - 1)],
                   "Die Hälfte von %d ist <b>%d</b>." % (2 * n, n))
    if kind == "fuesse":
        return mcq("%d Kinder stehen im Kreis. Wie viele Füße sind das?" % n, str(2 * n), [str(n), str(n + 2), str(4 * n)],
                   "Jedes Kind hat 2 Füße: %d + %d = <b>%d</b>." % (n, n, 2 * n))
    if kind == "kuchen":
        return mcq("Auf dem Blech sind %d Muffins. Die Hälfte wird verkauft. Wie viele Muffins sind noch da?" % (2 * n), str(n), [str(2 * n), str(n + 2), str(n - 1)],
                   "Die Hälfte von %d ist %d. Es bleiben <b>%d</b>." % (2 * n, n, n))
    return mcq("%s hatte gestern %d Sticker. Heute hat %s doppelt so viele. Wie viele Sticker hat %s heute?" % (p[0], n, p[1], p[1]), str(2 * n), [str(n + 2), str(n), str(2 * n + 2)],
               "Doppelt so viele: %d + %d = <b>%d</b>." % (n, n, 2 * n))


def main():
    seen = set()
    sets = [
        ("Verdoppeln mit Bildern", mix(R, seen, [(bild, 20)])),
        ("Verdopplungsaufgaben", mix(R, seen, [(dopp, 20)])),
        ("Halbieren", mix(R, seen, [(halb, 20)])),
        ("Fast verdoppeln", mix(R, seen, [(fast, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Verdoppeln</b> heißt: Die Zahl noch einmal dazu. Das Doppelte von 4 ist 4 + 4 = 8.",
         "<b>Halbieren</b> heißt: in zwei gleich große Teile teilen. Die Hälfte von 8 ist 4.",
         "Verdopplungsaufgaben helfen bei Nachbaraufgaben: 6 + 7 ist 1 mehr als 6 + 6.",
         "Mit einem Spiegel kannst du verdoppeln: Er zeigt alles zweimal."],
        [example("Das Doppelte von 7", ["7 + 7"], "14"),
         example("8 + 9", ["8 + 8 = 16", "1 mehr"], "17")],
        [["Das Doppelte von 6 ist 7", "6 + 6 = 12"],
         ["Beim Halbieren verdoppeln", "Halbieren macht die Zahl kleiner"],
         ["6 + 7 = 12", "6 + 6 = 12, dann 1 mehr: 13"]],
        extra=table(["Zahl", "Doppelt"], [["1", "2"], ["2", "4"], ["3", "6"], ["4", "8"], ["5", "10"], ["6", "12"], ["7", "14"], ["8", "16"], ["9", "18"], ["10", "20"]]))
    faq = [
        {"q": "Warum lernen Kinder Verdopplungsaufgaben?", "a": "Sie sind leicht zu merken und helfen bei vielen anderen Aufgaben, zum Beispiel 7 + 8 = 7 + 7 + 1."},
        {"q": "Welche Zahlen kann man halbieren?", "a": "In Klasse 1 nur gerade Zahlen wie 2, 4, 6 bis 20. Bei ungeraden Zahlen bleibt 1 übrig."},
        {"q": "Wie übt man Verdoppeln zu Hause?", "a": "Mit einem Spiegel und Plättchen, mit Würfelpaaren (Pasch) oder mit den Fingern beider Hände."},
        {"q": "Was ist eine Fast-Verdopplung?", "a": "Eine Aufgabe mit zwei Nachbarzahlen wie 5 + 6. Man rechnet 5 + 5 und noch 1 dazu."},
    ]
    make_unit(R, "verdoppeln-und-halbieren", "Z",
              "Die Schülerinnen und Schüler verdoppeln und halbieren Zahlen im Zahlenraum bis 20, nutzen Verdopplungsaufgaben für Nachbaraufgaben und lösen Sachaufgaben (Zusammenfassung).",
              "Verdoppeln und halbieren",
              "Verdoppeln und halbieren Klasse 1 – Arbeitsblätter mit Lösungen",
              "Verdoppeln und halbieren",
              "Verdoppeln und halbieren für Klasse 1: Verdoppeln mit Bildern, Verdopplungsaufgaben, Halbieren, Fast-Verdopplungen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Verdoppeln: 4 + 4 = 8",
              "Halbieren: Die Hälfte von 8 ist 4.",
              body, faq, sets, 9, grade="klasse-1")


if __name__ == "__main__":
    main()
