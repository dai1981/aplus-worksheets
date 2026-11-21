# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Zahlen bis 10（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_zahlen_bis_10.py
Zählen, Würfelbilder und Zehnerfeld, Zahlwörter, Nachbarzahlen und Zahlenreihe, Ordnungszahlen.
Fehler: ein Ding doppelt oder gar nicht gezählt, Vorgänger und Nachfolger verwechselt, Ordnungszahl von der falschen Seite gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, table
from de_k2 import de, KINDS, DING, ding
from k_pics import row_svg, scatter_svg, dice_svg, tenframe_svg, kinds_row_svg

R = random.Random(49401)
WORT = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn"]


def nah(n, lo=0, hi=10):
    return [str(x) for x in (n + 1, n - 1, n + 2, n - 2) if lo <= x <= hi and x != n]


def zaehlen():
    n = R.randint(1, 10)
    k = R.choice(KINDS)
    if R.random() < 0.5:
        pic = de(row_svg(n, k, per_row=5), ding(k, n))
    else:
        pic = de(scatter_svg(n, k, R.randint(1, 10 ** 6)), ding(k, n))
    return mcq(pic + "Wie viele %s sind es?" % DING[k][1], str(n), nah(n, 1),
               "Zeige auf jedes Ding und zähle: <b>%d</b>." % n)


def bilder():
    if R.random() < 0.5:
        n = R.randint(1, 6)
        a = R.randint(1, 6)
        if R.random() < 0.4 and n + a <= 10:
            return mcq(de(dice_svg([n, a]), "zwei Würfel mit %d und %d Augen" % (n, a)) + "Wie viele Punkte sind es zusammen?", str(n + a), nah(n + a, 2),
                       "%d und %d sind <b>%d</b>." % (n, a, n + a))
        return mcq(de(dice_svg([n]), "Würfel mit %d Augen" % n) + "Welche Zahl zeigt der Würfel?", str(n), nah(n, 1, 6),
                   "Das Würfelbild mit %d Punkten: <b>%d</b>." % (n, n))
    n = R.randint(1, 10)
    return mcq(de(tenframe_svg(n), "Zehnerfeld mit %d Punkten" % n) + "Wie viele Punkte sind im Zehnerfeld?", str(n), nah(n, 0),
               ("Oben 5, unten %d: 5 + %d = <b>%d</b>." % (n - 5, n - 5, n)) if n > 5 else "Die obere Reihe hat %d Punkte: <b>%d</b>." % (n, n))


def woerter():
    n = R.randint(0, 10)
    if R.random() < 0.5:
        return mcq("Welche Zahl ist „%s“?" % WORT[n], str(n), nah(n, 0), "„%s“ ist die <b>%d</b>." % (WORT[n].capitalize(), n))
    w = [WORT[x] for x in (n + 1, n - 1, n + 2) if 0 <= x <= 10]
    if n == 2:
        w.append("drei")
    return mcq("Wie heißt die Zahl %d als Wort?" % n, WORT[n], [x for x in dict.fromkeys(w + [WORT[(n + 5) % 11], WORT[(n + 3) % 11]]) if x != WORT[n]], "%d heißt <b>%s</b>." % (n, WORT[n]))


def reihe():
    kind = R.choice(["vor", "nach", "fehlt", "fehlt", "rueck"])
    if kind == "vor":
        n = R.randint(1, 10)
        return mcq("Welche Zahl kommt direkt <b>vor</b> der %d?" % n, str(n - 1), [str(n + 1)] + nah(n - 1, 0), "Eins weniger: <b>%d</b>." % (n - 1))
    if kind == "nach":
        n = R.randint(0, 9)
        return mcq("Welche Zahl kommt direkt <b>nach</b> der %d?" % n, str(n + 1), ([str(n - 1)] if n else []) + nah(n + 1, 0), "Eins mehr: <b>%d</b>." % (n + 1))
    if kind == "fehlt":
        s = R.randint(0, 6)
        k = R.randint(1, 3)
        seq = [str(s + i) if i != k else "?" for i in range(5)]
        return mcq("Welche Zahl fehlt? %s" % ", ".join(seq), str(s + k), nah(s + k, 0), "Die Zahlen gehen immer 1 weiter: <b>%d</b>." % (s + k))
    s = R.randint(5, 10)
    seq = [str(s - i) for i in range(4)] + ["?"]
    return mcq("Rückwärts zählen: %s" % ", ".join(seq), str(s - 4), nah(s - 4, 0), "Immer 1 weniger: <b>%d</b>." % (s - 4))


ORD = ["erste", "zweite", "dritte", "vierte", "fünfte", "sechste"]


def ordnung():
    ks = R.sample(KINDS, 6)
    i = R.randint(0, 5)
    side = R.choice(["links", "links", "rechts"])
    idx = i if side == "links" else 5 - i
    pic = de(kinds_row_svg(ks), "eine Reihe: " + ", ".join(DING[k][0] for k in ks))
    ans = DING[ks[idx]][0]
    other = DING[ks[5 - idx]][0] if 5 - idx != idx else DING[ks[(idx + 2) % 6]][0]
    w = [other] + [DING[ks[j]][0] for j in (idx - 1, idx + 1, idx + 2, idx - 2) if 0 <= j <= 5]
    return mcq(pic + "Was ist an %s Stelle von %s?" % (ORD[i] + "r", side), ans, list(dict.fromkeys(w)),
               "Zähle von %s: An %s Stelle ist <b>%s</b>." % (side, ORD[i] + "r", ans))


def main():
    seen = set()
    sets = [
        ("Zählen", mix(R, seen, [(zaehlen, 20)])),
        ("Würfelbilder und Zehnerfeld", mix(R, seen, [(bilder, 20)])),
        ("Zahlen und Zahlwörter", mix(R, seen, [(woerter, 20)])),
        ("Die Zahlenreihe", mix(R, seen, [(reihe, 20)])),
        ("Der Erste, der Zweite …", mix(R, seen, [(ordnung, 20)])),
    ]
    body = lesson(
        ["Beim Zählen zeigst du auf jedes Ding genau einmal.",
         "Die letzte Zahl sagt, wie viele es sind.",
         "Im Zehnerfeld siehst du die 5 schnell: Eine volle Reihe sind 5.",
         "Vor der 7 kommt die 6. Nach der 7 kommt die 8."],
        [example("Im Zehnerfeld: oben 5 Punkte, unten 3 Punkte", ["5 + 3"], "8"),
         example("Welche Zahl fehlt? 4, 5, ?, 7", ["immer 1 weiter"], "6")],
        [["Ein Ding zweimal zählen", "Jedes Ding nur einmal antippen"],
         ["Vor der 7 kommt die 8", "Vor der 7 kommt die 6"],
         ["Von der falschen Seite zählen", "Genau lesen: von links oder von rechts?"]],
        extra=table(["Zahl", "Wort"], [["1", "eins"], ["2", "zwei"], ["3", "drei"], ["4", "vier"], ["5", "fünf"], ["6", "sechs"], ["7", "sieben"], ["8", "acht"], ["9", "neun"], ["10", "zehn"]]))
    faq = [
        {"q": "Was ist ein Zehnerfeld?", "a": "Ein Feld mit 2 Reihen zu je 5 Kästchen. Kinder sehen damit schnell, wie viele es sind, ohne einzeln zu zählen."},
        {"q": "Warum Würfelbilder üben?", "a": "Würfelbilder erkennt man auf einen Blick. Das hilft beim schnellen Erfassen von Mengen und später beim Rechnen."},
        {"q": "Was sind Ordnungszahlen?", "a": "Zahlen für einen Platz in einer Reihe: der Erste, der Zweite, der Dritte. Man muss wissen, von welcher Seite gezählt wird."},
        {"q": "Wie übt man Zählen zu Hause?", "a": "Treppenstufen, Teller oder Socken zählen und dabei auf jedes Ding zeigen."},
    ]
    make_unit(R, "zahlen-bis-10", "Z",
              "Die Schülerinnen und Schüler zählen Mengen bis 10, erfassen Würfelbilder und Mengen im Zehnerfeld, lesen und schreiben Zahlen und Zahlwörter, kennen die Zahlenreihe und Ordnungszahlen (Zusammenfassung).",
              "Zahlen bis 10",
              "Zahlen bis 10 Klasse 1 – Arbeitsblätter mit Lösungen",
              "Zahlen bis 10",
              "Zahlen bis 10 für Klasse 1: Zählen, Würfelbilder, Zehnerfeld, Zahlwörter, Zahlenreihe und Ordnungszahlen. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Jedes Ding genau einmal zählen.",
              "Die letzte Zahl sagt, wie viele es sind.",
              body, faq, sets, 1, grade="klasse-1")


if __name__ == "__main__":
    main()
