# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Strichlisten und Tabellen（Leitidee Daten und Zufall）
  python3 tools/gen_de_mathe_k1_strichlisten_und_tabellen.py
Sortieren und zählen, Strichlisten lesen, mit Strichlisten vergleichen, Bilddiagramme, einfache Tabellen.
Fehler: ein Fünferbündel als 4 gezählt, Dinge doppelt gezählt, „wie viele mehr“ mit der ganzen Anzahl beantwortet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, strichliste, table
from de_k2 import de, KINDS, DING, ding, reihe
from k_pics import mixed_svg
from ws_common import fig

R = random.Random(49417)
OBST = ["Äpfel", "Bananen", "Birnen", "Erdbeeren", "Kirschen"]
TIERE = ["Hund", "Katze", "Hase", "Pferd", "Vogel"]


def fuenfer(n):
    parts = ["5"] * (n // 5) + ([str(n % 5)] if n % 5 else [])
    return " + ".join(parts)


def sortieren():
    ks = R.sample(KINDS, R.choice([2, 3]))
    counts = [(k, R.randint(2, 7)) for k in ks]
    if sum(n for _, n in counts) > 18:
        return None
    pic = de(mixed_svg(counts, R.randint(1, 10 ** 6)), "verschiedene Dinge durcheinander")
    k, n = R.choice(counts)
    if R.random() < 0.6:
        return mcq(pic + "Wie viele %s siehst du?" % DING[k][1], str(n), [str(n + 1), str(n - 1), str(sum(x for _, x in counts))],
                   "Zähle nur die %s. Streiche jedes gezählte Ding ab: <b>%d</b>." % (DING[k][1], n))
    mx = max(counts, key=lambda c: c[1])
    if [c[1] for c in counts].count(mx[1]) > 1:
        return None
    return mcq(pic + "Wovon gibt es am meisten?", DING[mx[0]][1], [DING[x][1] for x, _ in counts if x != mx[0]] + ["Von allen gleich viele", "Das kann man nicht sagen"],
               "Es sind %s. Am meisten sind es <b>%s</b>." % (", ".join(ding(x, c) for x, c in counts), DING[mx[0]][1]))


def lesen():
    n = R.randint(3, 20)
    return mcq(fig(strichliste(n)) + "Wie viele Striche sind es?", str(n), [str(n - n // 5) if n >= 5 else str(n + 2), str(n + 1), str(n - 1)],
               ("Ein Bündel mit Querstrich sind 5: %s = <b>%d</b>." % (fuenfer(n), n)) if n >= 5 else "Zähle die Striche: <b>%d</b>." % n)


def vergleich():
    cs = R.sample(OBST, 3)
    vals = R.sample(range(3, 15), 3)
    html = table(["Obst", "Strichliste"], [[c, strichliste(v)] for c, v in zip(cs, vals)])
    kind = R.choice(["wert", "meist", "mehr", "zusammen"])
    pre = "Die Kinder der Klasse 1a sagen, welches Obst sie am liebsten mögen." + html
    if kind == "wert":
        k = R.randrange(3)
        v = vals[k]
        return mcq(pre + "Wie viele Kinder mögen %s am liebsten?" % cs[k], str(v), [str(v - v // 5) if v >= 5 else str(v + 2), str(v + 1), str(vals[(k + 1) % 3])],
                   "%s = <b>%d</b>." % (fuenfer(v), v))
    if kind == "meist":
        k = vals.index(max(vals))
        return mcq(pre + "Welches Obst mögen die meisten Kinder?", cs[k], [c for c in cs if c != cs[k]] + ["Alle gleich viele"],
                   "Bei %s ist die Strichliste am längsten (%d): <b>%s</b>." % (cs[k], vals[k], cs[k]))
    if kind == "mehr":
        i, j = sorted(R.sample(range(3), 2), key=lambda x: -vals[x])
        d = vals[i] - vals[j]
        return mcq(pre + "Wie viele Kinder mehr mögen %s als %s?" % (cs[i], cs[j]), str(d), [str(vals[i]), str(d + 1), str(vals[i] + vals[j]) if vals[i] + vals[j] <= 30 else str(d + 2)],
                   "%d − %d = <b>%d</b>." % (vals[i], vals[j], d))
    i, j = R.sample(range(3), 2)
    t = vals[i] + vals[j]
    if t > 20:
        return None
    return mcq(pre + "Wie viele Kinder mögen %s oder %s am liebsten? Zähle zusammen." % (cs[i], cs[j]), str(t), [str(t + 1), str(t - 1), str(abs(vals[i] - vals[j]))],
               "%d + %d = <b>%d</b>." % (vals[i], vals[j], t))


def bild():
    ks = R.sample(KINDS, 3)
    vals = R.sample(range(1, 9), 3)
    pic = "".join(de(reihe(v, k, per_row=10), ding(k, v)) for k, v in zip(ks, vals))
    kind = R.choice(["meist", "wenig", "wert", "mehr"])
    if kind == "meist":
        k = vals.index(max(vals))
        return mcq(pic + "Wovon gibt es am meisten?", DING[ks[k]][1], [DING[x][1] for x in ks if x != ks[k]] + ["Von allen gleich viele"],
                   "Die längste Reihe hat %d: <b>%s</b>." % (vals[k], DING[ks[k]][1]))
    if kind == "wenig":
        k = vals.index(min(vals))
        return mcq(pic + "Wovon gibt es am wenigsten?", DING[ks[k]][1], [DING[x][1] for x in ks if x != ks[k]] + ["Von allen gleich viele"],
                   "Die kürzeste Reihe hat %d: <b>%s</b>." % (vals[k], DING[ks[k]][1]))
    if kind == "wert":
        k = R.randrange(3)
        return mcq(pic + "Wie viele %s sind es?" % DING[ks[k]][1], str(vals[k]), [str(vals[k] + 1), str(vals[k] - 1) if vals[k] > 1 else str(vals[k] + 2), str(sum(vals))],
                   "Zähle die Reihe: <b>%d</b>." % vals[k])
    i, j = sorted(R.sample(range(3), 2), key=lambda x: -vals[x])
    d = vals[i] - vals[j]
    return mcq(pic + "Wie viele %s sind es mehr als %s?" % (DING[ks[i]][1], DING[ks[j]][1]), str(d), [str(vals[i]), str(d + 1), str(vals[i] + vals[j])],
               "%d − %d = <b>%d</b>." % (vals[i], vals[j], d))


def tabelle():
    cs = R.sample(TIERE, 4)
    vals = R.sample(range(1, 12), 4)
    html = table(["Lieblingstier", "Kinder"], [[c, str(v)] for c, v in zip(cs, vals)])
    kind = R.choice(["wert", "meist", "wenig", "zusammen"])
    pre = "Umfrage in der Klasse 1b:" + html
    if kind == "wert":
        k = R.randrange(4)
        return mcq(pre + "Wie viele Kinder haben „%s“ gesagt?" % cs[k], str(vals[k]), [str(x) for x in vals if x != vals[k]], "In der Zeile „%s“ steht <b>%d</b>." % (cs[k], vals[k]))
    if kind == "meist":
        k = vals.index(max(vals))
        return mcq(pre + "Welches Tier haben die meisten Kinder gewählt?", cs[k], [c for c in cs if c != cs[k]], "Die größte Zahl ist %d: <b>%s</b>." % (vals[k], cs[k]))
    if kind == "wenig":
        k = vals.index(min(vals))
        return mcq(pre + "Welches Tier haben die wenigsten Kinder gewählt?", cs[k], [c for c in cs if c != cs[k]], "Die kleinste Zahl ist %d: <b>%s</b>." % (vals[k], cs[k]))
    i, j = R.sample(range(4), 2)
    t = vals[i] + vals[j]
    if t > 20:
        return None
    return mcq(pre + "Wie viele Kinder haben „%s“ oder „%s“ gesagt?" % (cs[i], cs[j]), str(t), [str(t + 1), str(t - 1), str(abs(vals[i] - vals[j])) if vals[i] != vals[j] else str(t + 2)],
               "%d + %d = <b>%d</b>." % (vals[i], vals[j], t))


def main():
    seen = set()
    sets = [
        ("Sortieren und zählen", mix(R, seen, [(sortieren, 20)])),
        ("Strichlisten lesen", mix(R, seen, [(lesen, 18), (vergleich, 2)])),
        ("Mit Strichlisten vergleichen", mix(R, seen, [(vergleich, 20)])),
        ("Bilddiagramme", mix(R, seen, [(bild, 20)])),
        ("Tabellen", mix(R, seen, [(tabelle, 20)])),
    ]
    body = lesson(
        ["Beim <b>Sortieren</b> legst du gleiche Dinge zusammen. Dann zählst du jede Sorte.",
         "In einer <b>Strichliste</b> machst du für jedes Ding einen Strich. Der fünfte Strich geht quer durch die vier anderen.",
         "Ein Fünferbündel sind 5 Striche. So zählst du schneller: 5, 10, 15 …",
         "In einer <b>Tabelle</b> findest du die Zahl in der richtigen Zeile."],
        [example("Zwei Fünferbündel und 3 Striche", ["5 + 5 + 3"], "13"),
         example("Äpfel 8, Bananen 5", ["8 − 5"], "3 Kinder mehr mögen Äpfel")],
        [["Ein Fünferbündel als 4 zählen", "Der Querstrich zählt mit: 5"],
         ["Dinge doppelt zählen", "Jedes gezählte Ding abstreichen"],
         ["„Wie viele mehr?“ mit der größeren Zahl beantworten", "Unterschied ausrechnen"]])
    faq = [
        {"q": "Warum lernen Kinder Strichlisten?", "a": "Mit Strichlisten kann man schnell zählen, zum Beispiel bei einer Umfrage in der Klasse. Die Fünferbündel üben gleichzeitig das Rechnen in Fünferschritten."},
        {"q": "Was ist ein Bilddiagramm?", "a": "Für jedes Ding wird ein Bild gezeichnet. Die längste Reihe zeigt, wovon es am meisten gibt."},
        {"q": "Wie übt man das zu Hause?", "a": "Autos einer Farbe zählen und Striche machen oder Spielzeug sortieren und eine kleine Tabelle anlegen."},
        {"q": "Was ist eine Umfrage?", "a": "Man fragt alle Kinder dasselbe, zum Beispiel nach dem Lieblingstier, und zählt die Antworten."},
    ]
    make_unit(R, "strichlisten-und-tabellen", "D",
              "Die Schülerinnen und Schüler sortieren und zählen Dinge, erfassen Daten in Strichlisten, lesen Bilddiagramme und einfache Tabellen und vergleichen Anzahlen (Zusammenfassung).",
              "Strichlisten und Tabellen",
              "Strichlisten und Tabellen Klasse 1 – Arbeitsblätter mit Lösungen",
              "Strichlisten und Tabellen",
              "Strichlisten und Tabellen für Klasse 1: sortieren und zählen, Strichlisten lesen und vergleichen, Bilddiagramme und Tabellen. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Ein Fünferbündel sind 5 Striche.",
              "Sortieren, zählen, vergleichen.",
              body, faq, sets, 17, grade="klasse-1")


if __name__ == "__main__":
    main()
