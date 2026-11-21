# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Rauminhalte – Liter und Milliliter（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k4_rauminhalte.py
Kommaschreibweise (1,5 l = 1500 ml), umwandeln, rechnen und vergleichen, Messbecher ablesen, Sachaufgaben.
Fehler: 1 l = 100 ml, 1,5 l = 15 ml oder 1005 ml, Messbecher falsch abgelesen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, wrap, table
from de_k4_groessen import lesen, kleiner, groesser, rechnen, komma, u
from ws_common import line, text, INK, BLUE

R = random.Random(49111)
KIDS = Kids(R)


def becher(ml, top=1000, step=100):
    """Messbecher bis top ml, Striche alle step ml, gefüllt bis ml"""
    H, x0, y0, w = 160, 50, 14, 70
    Y = lambda v: y0 + H - v / float(top) * H
    s = ["<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='#bfe0f7'/>" % (x0, Y(ml), w, y0 + H - Y(ml)),
         "<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 4, y0 + H, x0 + w, y0 - 4, INK)]
    for v in range(0, top + 1, step):
        long = v % (step * 2) == 0 or step >= 250
        s.append(line(x0, Y(v), x0 + (18 if long else 10), Y(v), INK, 1.5))
        if long:
            s.append(text(x0 - 6, Y(v) + 4, num(v), 11, anchor="end", weight=600))
    s.append(text(x0 + w + 8, y0 + 6, "ml", 12, anchor="start"))
    return wrap(x0 + w + 40, y0 + H + 10, "".join(s), "Messbecher", lg=True)


def ablesen():
    top, step = R.choice([(1000, 100), (500, 50), (1000, 50)])
    ml = R.randint(1, top // step - 1) * step
    w = [ml + step, ml - step, ml // step * (100 if step == 50 else 10) if ml // step * (100 if step == 50 else 10) != ml else ml + 2 * step, ml * 2 if ml * 2 <= top else ml // 2]
    return mcq(becher(ml, top, step) + "Wie viel Milliliter sind im Messbecher?", u(ml, "ml"), [u(x, "ml") for x in w if x > 0 and x != ml],
               "Ein kleiner Strich bedeutet %d ml. Das Wasser steht bei <b>%s</b>." % (step, u(ml, "ml")))


def sache():
    p = KIDS.next()
    kind = R.choice(["glaeser", "flaschen", "badewanne", "saft", "eimer"])
    if kind == "glaeser":
        tot, g = R.choice([(1000, 200), (1500, 250), (2000, 250), (1000, 125), (1500, 300)])
        n = tot // g
        q = "Aus einer Flasche mit %s Saft werden Gläser mit je %s gefüllt. Wie viele Gläser werden voll?" % (komma(tot, 1000, "l"), u(g, "ml"))
        return mcq(q, "%d Gläser" % n, ["%d Gläser" % x for x in (n + 1, tot // 100 // g * 10 if tot // 100 // g else n * 2, n * 2) if x != n and x > 0],
                   "%s = %d ml. %d ml %s %d ml = <b>%d</b>." % (komma(tot, 1000, "l"), tot, tot, GETEILT, g, n))
    if kind == "flaschen":
        n, per = R.randint(3, 12), R.choice([330, 500, 750, 1500])
        tot = n * per
        q = "%s kauft %d Flaschen Wasser zu je %s. Wie viele Liter sind das?" % (p[0], n, u(per, "ml") if per < 1000 else komma(per, 1000, "l"))
        return mcq(q, komma(tot, 1000, "l"), [komma(x, 1000, "l") for x in (tot * 10, tot + per, n * 1000) if x != tot],
                   "%d %s %d ml = %s ml = <b>%s</b>." % (n, MAL, per, num(tot), komma(tot, 1000, "l")))
    if kind == "badewanne":
        tot = R.choice([150, 160, 180, 200])
        inn = R.choice([10, 12, 15, 20])
        if tot % inn:
            return None
        m = tot // inn
        q = "In eine Badewanne passen %s Wasser. Pro Minute laufen %s hinein. Wie lange dauert es, bis sie voll ist?" % (u(tot, "l"), u(inn, "l"))
        return mcq(q, "%d min" % m, ["%d min" % x for x in (m + 5, tot - inn, m * 2) if x != m and x > 0], "%d l %s %d l = <b>%d min</b>." % (tot, GETEILT, inn, m))
    if kind == "saft":
        have = R.choice([2000, 3000, 1500])
        n, g = R.randint(4, 9), R.choice([150, 200, 250])
        if n * g >= have:
            return None
        r = have - n * g
        q = "Für ein Fest gibt es %s Saft. %d Kinder trinken je %s. Wie viel Saft ist noch da?" % (komma(have, 1000, "l"), n, u(g, "ml"))
        return mcq(q, komma(r, 1000, "l"), [komma(x, 1000, "l") for x in (n * g, have - g, r + g) if x > 0 and x != r],
                   "%d %s %d ml = %d ml. %d ml − %d ml = %d ml = <b>%s</b>." % (n, MAL, g, n * g, have, n * g, r, komma(r, 1000, "l")))
    e, n = R.choice([5, 8, 10, 12]), R.randint(3, 9)
    tot = e * n
    q = "Zum Blumengießen trägt %s %d volle Gießkannen zu je %s. Wie viele Liter sind das?" % (p[0], n, u(e, "l"))
    return mcq(q, u(tot, "l"), [u(x, "l") for x in (e + n, tot + e, tot * 10) if x != tot], "%d %s %d l = <b>%d l</b>." % (n, MAL, e, tot))


def main():
    seen = set()
    k = lambda fn: fn(R, 1000, "l", "ml")
    sets = [
        ("Liter und Milliliter mit Komma", mix(R, seen, [(k(lesen), 20)])),
        ("Umwandeln", mix(R, seen, [(k(kleiner), 10), (k(groesser), 10)])),
        ("Messbecher ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Rechnen und vergleichen", mix(R, seen, [(k(rechnen), 20)])),
        ("Sachaufgaben mit Litern", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Rauminhalte (Hohlmaße) misst du in Liter (l) und Milliliter (ml). 1 l = 1000 ml.",
         "Ein halber Liter sind 500 ml, ein viertel Liter 250 ml.",
         "Mit Komma: 1,5 l = 1,500 l = 1 l 500 ml = 1500 ml. Hinter dem Komma stehen drei Stellen für die Milliliter.",
         "Am <b>Messbecher</b> schaust du zuerst, wie viel ein Strich bedeutet."],
        [example("2,250 l in ml", ["2 l = 2000 ml", "2000 ml + 250 ml"], "2250 ml"),
         example("1 l − 330 ml", ["1000 ml − 330 ml"], "670 ml")],
        [["1 l = 100 ml", "1 l = 1000 ml"],
         ["1,5 l = 1005 ml", "1,500 l = 1500 ml"],
         ["Jeden Strich als 100 ml lesen", "Erst die Schrittweite am Messbecher prüfen"]],
        extra=table(["Gefäß", "ungefähr"], [["Teelöffel", "5 ml"], ["Trinkglas", "200 ml"], ["Milchtüte", "1 l"], ["Eimer", "10 l"], ["Badewanne", "150 l"]]))
    faq = [
        {"q": "Was ist ein Hohlmaß?", "a": "Ein Maß dafür, wie viel in ein Gefäß hineinpasst, zum Beispiel Liter und Milliliter."},
        {"q": "Wie viel ist ein Milliliter?", "a": "Etwa so viel wie 20 Wassertropfen. 1000 ml sind 1 Liter."},
        {"q": "Wie liest man einen Messbecher ab?", "a": "Auf Augenhöhe schauen und zuerst bestimmen, wie viele Milliliter ein Strich bedeutet."},
        {"q": "Wiegt ein Liter Wasser 1 kg?", "a": "Ja, ungefähr. Das ist eine gute Vergleichsgröße beim Schätzen."},
    ]
    make_unit(R, "rauminhalte", "G",
              "Die Schülerinnen und Schüler messen und vergleichen Rauminhalte in l und ml, nutzen die Kommaschreibweise, lesen Messgefäße ab und lösen Sachaufgaben (Zusammenfassung).",
              "Rauminhalte: Liter und Milliliter",
              "Liter und Milliliter Klasse 4 – Hohlmaße, Arbeitsblätter mit Lösungen",
              "Liter und Milliliter",
              "Klasse 4: Liter und Milliliter umrechnen, Kommaschreibweise, Messbecher ablesen, rechnen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 l = 1000 ml",
              "1,5 l = 1500 ml, ein viertel Liter = 250 ml.",
              body, faq, sets, 11, grade="klasse-4")


if __name__ == "__main__":
    main()
