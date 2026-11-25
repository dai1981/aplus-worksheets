# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Maßstab – Pläne und Karten（Leitidee Größen und Messen / Raum und Form）
  python3 tools/gen_de_mathe_k4_massstab.py
Bedeutung von 1 : 100, wirkliche Länge berechnen, Länge im Plan berechnen, Vergrößerungen (10 : 1), Grundrisse und Karten.
Fehler: 1 : 100 heißt 1 cm = 100 m, mal statt geteilt, Einheiten nicht umgerechnet, Vergrößerung mit Verkleinerung verwechselt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, wrap, NB, table
from ws_common import line, text, INK, GREEN, FILL

R = random.Random(49114)
KIDS = Kids(R)
MASS = [(10, "1 cm", "10 cm"), (50, "1 cm", "50 cm"), (100, "1 cm", "1 m"), (200, "1 cm", "2 m"), (1000, "1 cm", "10 m"),
        (10000, "1 cm", "100 m"), (25000, "1 cm", "250 m"), (100000, "1 cm", "1 km")]


def laenge(cm):
    """cm in passender Einheit"""
    if cm >= 100000 and cm % 100000 == 0:
        return "%s%skm" % (num(cm // 100000), NB)
    if cm >= 100000:
        km, r = divmod(cm, 100000)
        return "%s%skm %s%sm" % (num(km), NB, num(r // 100), NB) if r % 100 == 0 else "%s%scm" % (num(cm), NB)
    if cm >= 100 and cm % 100 == 0:
        return "%s%sm" % (num(cm // 100), NB)
    if cm >= 100:
        return "%s%sm %s%scm" % (num(cm // 100), NB, num(cm % 100), NB)
    return "%s%scm" % (num(cm), NB)


def bedeutung():
    m, a, b = R.choice(MASS)
    ans = "%s im Plan sind %s in Wirklichkeit." % (a, b)
    w = ["%s im Plan sind %s in Wirklichkeit." % (a, laenge(m * 100)), "%s in Wirklichkeit sind %s im Plan." % (a, b),
         "%s im Plan sind %s in Wirklichkeit." % (a, laenge(max(m // 10, 1)) if m >= 100 else laenge(m * 10))]
    return mcq("Was bedeutet der Maßstab 1 : %s?" % num(m), ans, [x for x in w if x != ans],
               "1 : %s heißt: 1 cm im Plan sind %s cm = <b>%s</b> in Wirklichkeit." % (num(m), num(m), b))


def wirklich():
    m, a, b = R.choice(MASS[1:])
    plan = R.randint(2, 12)
    r = plan * m
    w = [plan * m // 100 if plan * m >= 10000 else plan * m * 10, plan + m, r * 10, r // 10]
    return mcq("Maßstab 1 : %s. Im Plan ist eine Strecke %d cm lang. Wie lang ist sie in Wirklichkeit?" % (num(m), plan), laenge(r),
               [laenge(x) for x in w if x > 0 and laenge(x) != laenge(r)],
               "%d %s %s cm = %s cm = <b>%s</b>." % (plan, MAL, num(m), num(r), laenge(r)))


def im_plan():
    m, a, b = R.choice(MASS[2:])
    plan = R.randint(2, 15)
    real = plan * m
    w = [plan * 10, plan * 100 if plan * 100 != plan else plan + 1, real, plan + 5]
    return mcq("Maßstab 1 : %s. In Wirklichkeit ist eine Strecke %s lang. Wie lang ist sie im Plan?" % (num(m), laenge(real)), "%d%scm" % (plan, NB),
               [("%s%scm" % (num(x), NB)) for x in w if x != plan],
               "%s = %s cm. %s cm %s %s = <b>%d cm</b>." % (laenge(real), num(real), num(real), GETEILT, num(m), plan))


def vergroesserung():
    f = R.choice([2, 5, 10])
    kind = R.choice(["real", "bild"])
    if kind == "real":
        real = R.randint(3, 20)
        bild = real * f
        if bild % 10:
            return None
        cm = bild // 10
        tier = R.choice(["Käfer", "Marienkäfer", "Grashüpfer", "Floh", "Schmetterling"])
        if tier == "Floh" and real > 4:
            return None
        q = "Ein %s ist im Sachbuch im Maßstab %d : 1 abgebildet. Im Bild ist er %d cm lang. Wie lang ist er in Wirklichkeit?" % (tier, f, cm)
        ans = "%d%smm" % (real, NB)
        w = ["%d%scm" % (cm * f, NB), "%d%smm" % (bild, NB), "%d%smm" % (cm, NB) if cm != real else None, "%d%scm" % (cm, NB)]
        e = "%d : 1 heißt: das Bild ist %d-mal so groß. %d cm = %d mm, %d mm %s %d = <b>%s</b>." % (f, f, cm, bild, bild, GETEILT, f, ans)
        w = [x for x in w if x]
    else:
        real = R.randint(2, 15)
        q = "Eine Ameise ist %d mm lang. Sie wird im Maßstab %d : 1 gezeichnet. Wie lang ist sie im Bild?" % (real, f)
        ans = "%d%smm" % (real * f, NB)
        w = ["%d%smm" % (real, NB), "%d%smm" % (real * f * 10, NB), "%d%smm" % (real + f, NB)]
        e = "Das Bild ist %d-mal so groß: %d mm %s %d = <b>%s</b>." % (f, real, MAL, f, ans)
    return mcq(q, ans, [x for x in w if x != ans], e)


def grundriss():
    m = R.choice([50, 100, 200])
    a, b = R.randint(3, 8), R.randint(2, 6)
    if a == b:
        return None
    k = 22
    s = ["<rect x='48' y='14' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (a * k, b * k, FILL, GREEN),
         text(48 + a * k / 2.0, 10, "%d cm" % a, 12), text(42, 14 + b * k / 2.0 + 4, "%d cm" % b, 12, anchor="end")]
    pic = wrap(a * k + 70, b * k + 30, "".join(s), "Grundriss eines Zimmers", lg=True)
    which = R.choice(["lang", "breit"])
    v = a if which == "lang" else b
    r = v * m
    q = pic + "Grundriss eines Zimmers im Maßstab 1 : %d. Wie %s ist das Zimmer in Wirklichkeit?" % (m, which)
    return mcq(q, laenge(r), [laenge(x) for x in (v * m // 10, v * m * 10, (a if which == "breit" else b) * m) if laenge(x) != laenge(r)],
               "%d cm %s %d = %d cm = <b>%s</b>." % (v, MAL, m, r, laenge(r)))


def karte():
    m = R.choice([25000, 50000, 100000])
    p = KIDS.next()
    cm = R.randint(2, 12)
    r = cm * m
    q = "%s misst auf einer Wanderkarte im Maßstab 1 : %s eine Strecke von %d cm. Wie weit ist der Weg in Wirklichkeit?" % (p[0], num(m), cm)
    return mcq(q, laenge(r), [laenge(x) for x in (r // 10, r * 10, cm * 1000) if laenge(x) != laenge(r)],
               "%d %s %s cm = %s cm = <b>%s</b>." % (cm, MAL, num(m), num(r), laenge(r)))


def main():
    seen = set()
    sets = [
        ("Was bedeutet der Maßstab?", mix(R, seen, [(bedeutung, 8), (wirklich, 12)])),
        ("Wirkliche Länge berechnen", mix(R, seen, [(wirklich, 20)])),
        ("Länge im Plan berechnen", mix(R, seen, [(im_plan, 20)])),
        ("Vergrößerungen", mix(R, seen, [(vergroesserung, 20)])),
        ("Grundrisse und Karten", mix(R, seen, [(grundriss, 12), (karte, 8)])),
    ]
    body = lesson(
        ["Ein <b>Maßstab</b> sagt, wie stark etwas verkleinert oder vergrößert gezeichnet ist.",
         "1 : 100 heißt: 1 cm im Plan sind 100 cm = 1 m in Wirklichkeit. Die Wirklichkeit ist 100-mal so groß.",
         "Wirkliche Länge = Länge im Plan mal die Maßstabszahl. Länge im Plan = wirkliche Länge geteilt durch die Maßstabszahl.",
         "10 : 1 ist eine <b>Vergrößerung</b>: Das Bild ist 10-mal so groß wie die Wirklichkeit."],
        [example("Maßstab 1 : 200, im Plan 4 cm", ["4 %s 200 cm = 800 cm" % MAL], "8 m"),
         example("Maßstab 1 : 100 000, auf der Karte 3 cm", ["3 %s 100 000 cm = 300 000 cm" % MAL], "3 km")],
        [["1 : 100 heißt 1 cm = 100 m", "1 cm = 100 cm = 1 m"],
         ["Plan → Wirklichkeit mit geteilt rechnen", "Zur Wirklichkeit hin malnehmen"],
         ["10 : 1 als Verkleinerung lesen", "Steht die größere Zahl vorne, ist es eine Vergrößerung"]],
        extra=table(["Maßstab", "1 cm im Plan sind"], [["1 : 100", "1 m"], ["1 : 1000", "10 m"], ["1 : 100 000", "1 km"]]))
    faq = [
        {"q": "Wo braucht man den Maßstab?", "a": "Bei Landkarten, Stadtplänen, Grundrissen von Wohnungen und Bauplänen, aber auch bei Vergrößerungen von kleinen Tieren im Sachbuch."},
        {"q": "Wie rechnet man mit dem Maßstab?", "a": "Bei 1 : 100 nimmt man jede Länge im Plan mal 100, um die wirkliche Länge zu erhalten. Umgekehrt teilt man durch 100."},
        {"q": "Warum muss man oft Einheiten umrechnen?", "a": "Weil das Ergebnis in cm sehr groß wird. 300 000 cm schreibt man besser als 3 km."},
        {"q": "Was bedeutet 2 : 1?", "a": "Das Bild ist doppelt so groß wie in Wirklichkeit."},
    ]
    make_unit(R, "massstab", "G",
              "Die Schülerinnen und Schüler verstehen Maßstabsangaben bei Verkleinerungen und Vergrößerungen, berechnen Längen in Plänen, Grundrissen und Karten und rechnen dabei Einheiten um (Zusammenfassung).",
              "Maßstab: Pläne, Grundrisse und Karten",
              "Maßstab Klasse 4 – Arbeitsblätter mit Lösungen",
              "Maßstab",
              "Maßstab für Klasse 4: 1 : 100 verstehen, wirkliche Länge und Länge im Plan berechnen, Vergrößerungen, Grundrisse und Karten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 : 100 heißt: 1 cm im Plan sind 1 m in Wirklichkeit.",
              "Zur Wirklichkeit malnehmen, zum Plan teilen.",
              body, faq, sets, 14, grade="klasse-4")


if __name__ == "__main__":
    main()
