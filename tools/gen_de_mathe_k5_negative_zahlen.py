# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Negative Zahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_negative_zahlen.py
Thermometer ablesen, Zahlengerade mit negativen Zahlen, vergleichen und ordnen, Temperaturänderungen, Sachaufgaben (Kontostand, Stockwerke).
Fehler: −8 für größer als −3 gehalten, beim Unterschied über die 0 subtrahiert statt addiert, Richtung auf der Zahlengerade verwechselt.
"""
import random
import functools
from de_common import mcq as _mcq, num, lesson, example, make_unit, mix, wrap, zahlenstrahl
from ws_common import line, text, INK, RED

R = random.Random(49503)
mcq = functools.partial(_mcq, neg=True)
LT, GT = "&lt;", "&gt;"


def g(v):
    return "%s °C" % num(v)


def thermo_svg(t, lo=-20, hi=30):
    H = 240
    y = lambda v: 20 + (hi - v) / float(hi - lo) * H
    s = ["<rect x='60' y='14' width='16' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (H + 12, INK),
         "<circle cx='68' cy='%d' r='14' fill='%s'/>" % (H + 34, RED),
         "<rect x='63' y='%.1f' width='6' height='%.1f' fill='%s'/>" % (y(t), H + 30 - y(t), RED)]
    for v in range(lo, hi + 1, 2):
        big = v % 10 == 0
        s.append(line(76, y(v), 76 + (14 if big else 8), y(v), INK, 1.4 if big else 0.9))
        if big:
            s.append(text(96, y(v) + 5, num(v), 13, anchor="start", weight=600))
    return wrap(140, H + 60, "".join(s), "Thermometer", lg=True)


def thermo():
    t = R.choice([x for x in range(-18, 29, 2) if x != 0])
    return mcq(thermo_svg(t) + "Welche Temperatur zeigt das Thermometer?", g(t), [g(-t), g(t + 2), g(t - 2)],
               "Ein kleiner Strich bedeutet 2 °C. %s" % ("Die Säule endet unter der 0: <b>%s</b>." % g(t) if t < 0 else "Die Säule endet über der 0: <b>%s</b>." % g(t)))


def gerade():
    step = R.choice([1, 1, 2, 5])
    lo = -10 * step
    v = R.choice([x for x in range(lo + step, -lo, step) if x != 0 and x % (5 * step)])
    pic = zahlenstrahl(lo, -lo, step, marks=[(v, "A")], every=5 * step, label="Zahlengerade")
    return mcq(pic + "Welche Zahl gehört zum Pfeil A?", num(v), [num(-v), num(v + step), num(v - step)],
               "Links von der 0 liegen die negativen Zahlen. Ein Strich bedeutet %d: <b>%s</b>." % (step, num(v)))


def vergleich():
    kind = R.choice(["satz", "satz", "ordnen", "groesste"])
    if kind == "satz":
        a, b = R.sample(range(-20, 21), 2)
        if a >= 0 and b >= 0:
            return None
        sym = LT if a < b else GT
        ans = "%s %s %s" % (num(a), sym, num(b))
        w = ["%s %s %s" % (num(a), GT if sym == LT else LT, num(b)), "%s = %s" % (num(a), num(b)), "%s %s %s" % (num(b), sym, num(a))]
        return mcq("Welcher Satz stimmt? (%s und %s)" % (num(a), num(b)), ans, w, "Auf der Zahlengerade liegt %s weiter links: <b>%s</b>." % (num(min(a, b)), ans))
    nums = R.sample([x for x in range(-25, 26) if x], 4)
    if not any(x < 0 for x in nums):
        return None
    if kind == "ordnen":
        s = sorted(nums)
        ans = " &lt; ".join(num(x) for x in s)
        w = [" &lt; ".join(num(x) for x in sorted(nums, key=lambda x: (abs(x), x))), " &lt; ".join(num(x) for x in s[::-1]), " &lt; ".join(num(x) for x in [s[1], s[0], s[2], s[3]])]
        return mcq("Ordne von klein nach groß: %s" % ", ".join(num(x) for x in nums), ans, [x for x in w if x != ans] + [" &lt; ".join(num(x) for x in [s[0], s[2], s[1], s[3]])],
                   "Je weiter links auf der Zahlengerade, desto kleiner: <b>%s</b>." % ans)
    return mcq("Welche Zahl ist am kleinsten? %s" % ", ".join(num(x) for x in nums), num(min(nums)),
               [num(x) for x in nums if x != min(nums)], "Am weitesten links liegt <b>%s</b>." % num(min(nums)))


def aenderung():
    kind = R.choice(["steigt", "faellt", "diff"])
    if kind == "steigt":
        a, d = R.randint(-15, -1), R.randint(2, 20)
        r = a + d
        return mcq("Am Morgen sind es %s. Bis Mittag steigt die Temperatur um %d °C. Wie warm ist es mittags?" % (g(a), d), g(r),
                   [g(a - d), g(-(r)) if r else g(d - a), g(r + 2)], "Von %s aus %d nach oben: <b>%s</b>." % (g(a), d, g(r)))
    if kind == "faellt":
        a, d = R.randint(-5, 10), R.randint(3, 15)
        r = a - d
        if r >= 0:
            return None
        return mcq("Am Abend sind es %s. In der Nacht fällt die Temperatur um %d °C. Wie kalt ist es nachts?" % (g(a), d), g(r),
                   [g(-r), g(a + d), g(r - 2)], "Von %s aus %d nach unten: <b>%s</b>." % (g(a), d, g(r)))
    a, b = R.randint(-15, -1), R.randint(1, 20)
    d = b - a
    return mcq("Nachts waren es %s, mittags %s. Um wie viel Grad ist es wärmer geworden?" % (g(a), g(b)), "%d °C" % d,
               ["%d °C" % x for x in (b + a if b + a > 0 else abs(b + a) + 1, d + 1, b)], "Von %s bis 0 sind es %d, von 0 bis %s noch %d: <b>%d °C</b>." % (g(a), -a, g(b), b, d))


def sache():
    kind = R.choice(["konto", "aufzug", "tauchen", "konto2"])
    if kind == "konto":
        a, d = R.randint(10, 80), R.randint(20, 150)
        r = a - d
        if r >= 0:
            return None
        return mcq("Auf einem Konto sind %d €. Es werden %d € abgebucht. Wie hoch ist der Kontostand jetzt?" % (a, d), "%s €" % num(r),
                   ["%s €" % num(x) for x in (-r, a + d, r - 10)], "%d − %d = <b>%s €</b>. Das Konto ist im Minus." % (a, d, num(r)))
    if kind == "konto2":
        a, d = R.randint(-120, -10), R.randint(20, 200)
        r = a + d
        return mcq("Der Kontostand ist %s €. Dann kommen %d € dazu. Wie hoch ist der Kontostand jetzt?" % (num(a), d), "%s €" % num(r),
                   ["%s €" % num(x) for x in (a - d, -r if r else 10, r + 10)], "%s + %d = <b>%s €</b>." % (num(a), d, num(r)))
    if kind == "aufzug":
        a, d = R.randint(-3, 6), R.randint(2, 8)
        r = a - d
        if r < -4:
            return None
        return mcq("Ein Aufzug ist im Stockwerk %s. Er fährt %d Stockwerke nach unten. In welchem Stockwerk ist er jetzt?" % (num(a), d), num(r),
                   [num(x) for x in (a + d, -r if r else 1, r + 1)], "%s − %d = <b>%s</b>. Negative Stockwerke liegen unter der Erde." % (num(a), d, num(r)))
    a, d = R.randint(-30, -5), R.randint(3, 20)
    r = a + d
    if r >= 0:
        return None
    return mcq("Ein Taucher ist %d m unter dem Meeresspiegel (%s m). Er steigt %d m nach oben. Wo ist er jetzt?" % (-a, num(a), d), "%s m" % num(r),
               ["%s m" % num(x) for x in (a - d, -r, r - 1)], "%s + %d = <b>%s m</b>." % (num(a), d, num(r)))


def main():
    seen = set()
    sets = [
        ("Thermometer ablesen", mix(R, seen, [(thermo, 20)])),
        ("Die Zahlengerade", mix(R, seen, [(gerade, 20)])),
        ("Vergleichen und ordnen", mix(R, seen, [(vergleich, 20)])),
        ("Temperaturänderungen", mix(R, seen, [(aenderung, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zahlen unter 0 heißen <b>negative Zahlen</b>. Man schreibt ein Minuszeichen davor: −5.",
         "Auf der Zahlengerade liegen die negativen Zahlen links von der 0.",
         "Je weiter links eine Zahl liegt, desto kleiner ist sie: −8 &lt; −3.",
         "Geht es über die 0, rechnest du in zwei Schritten: von −4 °C bis 0 °C sind es 4, dann weiter."],
        [example("Von −6 °C auf 9 °C", ["bis 0: 6", "bis 9: 9", "6 + 9"], "15 °C wärmer"),
         example("−8 und −3 vergleichen", ["−8 liegt weiter links"], "−8 &lt; −3")],
        [["−8 &gt; −3, weil 8 größer als 3 ist", "Bei negativen Zahlen ist −8 kleiner"],
         ["Unterschied von −6 bis 9 = 3", "Über die 0: 6 + 9 = 15"],
         ["Bei „fällt“ nach rechts gehen", "Fallen = nach links (kleiner)"]])
    faq = [
        {"q": "Wo begegnen Kinder negativen Zahlen?", "a": "Beim Thermometer im Winter, beim Kontostand, bei Stockwerken unter der Erde und bei Höhen unter dem Meeresspiegel."},
        {"q": "Warum ist −8 kleiner als −3?", "a": "Auf der Zahlengerade liegt −8 weiter links. Bei Temperaturen ist −8 °C auch kälter als −3 °C."},
        {"q": "Wann lernt man negative Zahlen?", "a": "Je nach Bundesland in Klasse 5 oder 6 als Einführung. Das Rechnen mit ganzen Zahlen wird in Klasse 6 oder 7 vertieft."},
        {"q": "Wie berechnet man Temperaturunterschiede über die 0?", "a": "In zwei Schritten: vom negativen Wert bis 0 und dann von 0 bis zum positiven Wert. Beide Teile addiert man."},
    ]
    make_unit(R, "negative-zahlen", "Z",
              "Die Schülerinnen und Schüler lesen negative Zahlen in Sachsituationen ab, stellen sie an der Zahlengerade dar, vergleichen und ordnen sie und beschreiben Änderungen, auch über die Null hinweg (Zusammenfassung).",
              "Negative Zahlen",
              "Negative Zahlen Klasse 5 – Arbeitsblätter mit Lösungen",
              "Negative Zahlen",
              "Negative Zahlen für Klasse 5: Thermometer, Zahlengerade, vergleichen und ordnen, Temperaturänderungen, Kontostand und Stockwerke. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Je weiter links, desto kleiner.",
              "−8 < −3",
              body, faq, sets, 3, grade="klasse-5")


if __name__ == "__main__":
    main()
