# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Zahlen zerlegen und ergänzen bis 10（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_zerlegen_und_ergaenzen.py
Zerlegen (Teil – Teil – Ganzes), Schüttelbox mit roten und blauen Plättchen, bis 10 ergänzen, versteckte Dinge, Zahlenhäuser.
Fehler: das Ganze statt des fehlenden Teils angegeben, um 1 verzählt, Teile addiert statt ergänzt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, table
from de_k2 import de, KINDS, DING, ding
from k_pics import bond_svg, tenframe_mix_svg, tenframe_svg, box_svg

R = random.Random(49404)


def w3(x, hi=10):
    return [str(v) for v in (x + 1, x - 1, x + 2, x - 2) if 0 <= v <= hi and v != x]


def zerlegen():
    n = R.randint(3, 10)
    a = R.randint(1, n - 1)
    b = n - a
    kind = R.choice(["teil", "teil", "ganz"])
    if kind == "teil":
        pic = de(bond_svg(n, a, "?"), "Zerlegung: %d besteht aus %d und einem fehlenden Teil" % (n, a))
        return mcq(pic + "Welche Zahl fehlt?", str(b), [str(n)] + w3(b), "%d und <b>%d</b> sind zusammen %d." % (a, b, n))
    pic = de(bond_svg("?", a, b), "Zerlegung: %d und %d, das Ganze fehlt" % (a, b))
    return mcq(pic + "Welche Zahl fehlt oben?", str(n), [str(abs(a - b)) if a != b else str(n + 2)] + w3(n), "%d und %d sind zusammen <b>%d</b>." % (a, b, n))


def schuettel():
    n = R.randint(4, 10)
    r = R.randint(1, n - 1)
    cells = ["r"] * r + ["b"] * (n - r) + [""] * (10 - n)
    pic = de(tenframe_mix_svg(cells), "Zehnerfeld mit %d roten und %d blauen Plättchen" % (r, n - r))
    if R.random() < 0.5:
        return mcq(pic + "%d rote Plättchen und wie viele blaue? Zusammen sind es %d." % (r, n), str(n - r), [str(n)] + w3(n - r),
                   "%d + <b>%d</b> = %d." % (r, n - r, n))
    return mcq(pic + "Wie viele Plättchen sind es zusammen?", str(n), [str(abs(n - 2 * r)) if n != 2 * r else str(n + 2)] + w3(n),
               "%d rote und %d blaue: %d + %d = <b>%d</b>." % (r, n - r, r, n - r, n))


def bis10():
    n = R.randint(1, 9)
    if R.random() < 0.6:
        pic = de(tenframe_svg(n), "Zehnerfeld mit %d Punkten" % n)
        return mcq(pic + "Wie viele Punkte fehlen bis 10?", str(10 - n), [str(n)] + w3(10 - n), "%d + <b>%d</b> = 10. Zähle die leeren Kästchen." % (n, 10 - n))
    if R.random() < 0.5:
        return mcq("? + %d = 10" % n, str(10 - n), [str(n)] + w3(10 - n), "<b>%d</b> und %d sind zusammen 10." % (10 - n, n))
    return mcq("%d + ? = 10" % n, str(10 - n), [str(n)] + w3(10 - n), "%d und <b>%d</b> sind zusammen 10." % (n, 10 - n))


def kiste():
    k = R.choice(KINDS)
    total = R.randint(4, 10)
    seen_n = R.randint(1, total - 1)
    pic = de(box_svg(seen_n, k), "%s und eine geschlossene Kiste" % ding(k, seen_n))
    return mcq(pic + "Zusammen sind es %d %s. Wie viele sind in der Kiste?" % (total, DING[k][1]), str(total - seen_n),
               [str(total), str(seen_n) if seen_n != total - seen_n else str(total + 1)] + w3(total - seen_n),
               "%d + ? = %d. In der Kiste sind <b>%d</b>." % (seen_n, total, total - seen_n))


def haus():
    n = R.randint(4, 10)
    kind = R.choice(["passt", "nicht", "wie_viele"])
    if kind == "passt":
        a = R.randint(0, n)
        ans = "%d + %d" % (a, n - a)
        w = ["%d + %d" % (a, n - a + 1), "%d + %d" % (a + 1, n - a + 1) if n - a + 1 <= 10 else "%d + %d" % (a, n - a - 1) if n - a >= 1 else "%d + %d" % (a + 2, 1), "%d + %d" % (max(a - 1, 0), n - a - 1 if n - a >= 1 else 2)]
        return mcq("Welche Zerlegung gehört ins Zahlenhaus %d?" % n, ans, [x for x in dict.fromkeys(w) if x != ans and eval(x) != n] + ["%d + %d" % (n, 1)],
                   "%s = %d: <b>%s</b>." % (ans, n, ans))
    if kind == "nicht":
        goods = ["%d + %d" % (a, n - a) for a in range(1, n)]
        if len(goods) < 3:
            return None
        g = R.sample(goods, 3)
        a = R.randint(1, n - 1)
        bad = "%d + %d" % (a, n - a + R.choice([1, -1]) if n - a > 1 else n - a + 1)
        return mcq("Welche Aufgabe gehört <b>nicht</b> ins Zahlenhaus %d?" % n, bad, g, "%s ist nicht %d. <b>%s</b> gehört nicht dazu." % (bad, n, bad))
    k = n + 1
    return mcq("Wie viele Zerlegungen hat die %d, wenn man 0 + %d und %d + 0 mitzählt?" % (n, n, n), str(k), [str(n), str(n - 1), str(k + 1)],
               "Von 0 + %d bis %d + 0 sind es <b>%d</b> Zerlegungen." % (n, n, k))


def main():
    seen = set()
    sets = [
        ("Zahlen zerlegen", mix(R, seen, [(zerlegen, 20)])),
        ("Rote und blaue Plättchen", mix(R, seen, [(schuettel, 20)])),
        ("Bis 10 ergänzen", mix(R, seen, [(bis10, 20)])),
        ("Was ist in der Kiste?", mix(R, seen, [(kiste, 20)])),
        ("Zahlenhäuser", mix(R, seen, [(haus, 20)])),
    ]
    body = lesson(
        ["Eine Zahl kann man in zwei Teile <b>zerlegen</b>: 7 = 3 + 4 oder 7 = 5 + 2.",
         "Kennst du das Ganze und einen Teil, findest du den anderen Teil durch <b>Ergänzen</b>: 3 + ? = 7.",
         "Die Partner der 10 sind besonders wichtig: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.",
         "Im Zahlenhaus stehen oben die Zahl und darunter alle Zerlegungen."],
        [example("Das Ganze ist 8, ein Teil ist 5", ["5 + ? = 8"], "3"),
         example("Im Zehnerfeld sind 6 Punkte", ["6 + ? = 10"], "4 fehlen")],
        [["Beim fehlenden Teil das Ganze hinschreiben", "Gesucht ist nur der fehlende Teil"],
         ["5 + ? = 8 → 13", "Ergänzen, nicht addieren: 3"],
         ["Um 1 verzählen", "Mit dem Zehnerfeld prüfen"]],
        extra=table(["Zahl", "Zerlegungen"], [["5", "1 + 4, 2 + 3, 3 + 2, 4 + 1"], ["10", "1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5"]]))
    faq = [
        {"q": "Warum ist das Zerlegen so wichtig?", "a": "Wer Zahlen sicher zerlegen kann, rechnet später schnell über die 10: 8 + 5 = 8 + 2 + 3."},
        {"q": "Was ist eine Schüttelbox?", "a": "Eine Schachtel mit Plättchen, die auf einer Seite rot und auf der anderen blau sind. Nach dem Schütteln zählt man die roten und die blauen."},
        {"q": "Was ist ein Zahlenhaus?", "a": "Oben im Dach steht eine Zahl, in den Stockwerken stehen ihre Zerlegungen, zum Beispiel 6 = 1 + 5, 2 + 4, 3 + 3."},
        {"q": "Wie übt man die Partner der 10?", "a": "Mit den Fingern: 3 Finger oben, wie viele sind unten? Oder mit dem Zehnerfeld."},
    ]
    make_unit(R, "zerlegen-und-ergaenzen", "Z",
              "Die Schülerinnen und Schüler zerlegen Zahlen bis 10 in Teilmengen, ergänzen bis 10, finden alle Zerlegungen einer Zahl und nutzen den Zusammenhang von Teil und Ganzem (Zusammenfassung).",
              "Zahlen zerlegen und ergänzen",
              "Zahlen zerlegen Klasse 1 – Arbeitsblätter mit Lösungen",
              "Zerlegen und ergänzen",
              "Zahlen zerlegen und ergänzen für Klasse 1: Teil und Ganzes, Schüttelbox, Partner der 10, versteckte Dinge und Zahlenhäuser. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "7 = 3 + 4 = 5 + 2 = 6 + 1",
              "Die Partner der 10 sicher kennen.",
              body, faq, sets, 4, grade="klasse-1")


if __name__ == "__main__":
    main()
