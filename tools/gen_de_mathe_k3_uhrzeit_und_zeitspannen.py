# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Uhrzeit und Zeitspannen（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k3_uhrzeit_und_zeitspannen.py
Uhr ablesen, Uhrzeiten in Worten (halb vier = 3:30), 24-Stunden-Zählung, Zeitspannen, Zeiteinheiten und Sachaufgaben.
Fehler: „halb vier“ als 4:30, Stunden- und Minutenzeiger vertauscht, 1 h = 100 min, Zeitspanne über die volle Stunde falsch.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, clock, table

R = random.Random(49014)
KIDS = Kids(R)
ZAHL = ["zwölf", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf"]


def hm(h, m):
    return "%d:%02d Uhr" % (h, m)


def dauer(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return "%d h %d min" % (h, m)
    return "%d h" % h if h else "%d min" % m


def ablesen():
    h = R.randint(1, 12)
    m = R.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]) if R.random() < 0.75 else R.randint(1, 59)
    hh = h
    w = [hm(m // 5 if m // 5 else 12, h * 5 % 60) if m % 5 == 0 and (m // 5) != h else None,
         hm(h % 12 + 1, m), hm(h, (m + 5) % 60) if m < 55 else hm(h, m - 5), hm(h - 1 if h > 1 else 12, m)]
    return mcq(clock(h, m) + "Wie spät ist es?", hm(hh, m), [x for x in w if x and x != hm(hh, m)],
               "Der kurze Zeiger zeigt die Stunde (%d), der lange Zeiger die Minuten (%d). Es ist <b>%s</b>." % (h, m, hm(hh, m)))


def worte():
    h = R.randint(1, 12)
    kind = R.choice(["halb", "halb", "viertel nach", "viertel vor", "nach", "vor"])
    nxt = h % 12 + 1
    if kind == "halb":
        phrase, ans = "halb %s" % ZAHL[nxt], hm(h, 30)
        w = [hm(nxt, 30), hm(h, 50), hm(nxt, 0)]
        e = "„Halb %s“ heißt: eine halbe Stunde <b>vor</b> %s Uhr, also <b>%s</b>." % (ZAHL[nxt], ZAHL[nxt], ans)
    elif kind == "viertel nach":
        phrase, ans = "Viertel nach %s" % ZAHL[h], hm(h, 15)
        w = [hm(h, 45), hm(h - 1 if h > 1 else 12, 45), hm(h, 4)]
        e = "Viertel nach heißt 15 Minuten nach der vollen Stunde: <b>%s</b>." % ans
    elif kind == "viertel vor":
        phrase, ans = "Viertel vor %s" % ZAHL[nxt], hm(h, 45)
        w = [hm(nxt, 15), hm(nxt, 45), hm(h, 15)]
        e = "Viertel vor %s heißt 15 Minuten vor %s Uhr: <b>%s</b>." % (ZAHL[nxt], ZAHL[nxt], ans)
    elif kind == "nach":
        mm = R.choice([5, 10, 20])
        word = {5: "fünf", 10: "zehn", 20: "zwanzig"}[mm]
        phrase, ans = "%s nach %s" % (word, ZAHL[h]), hm(h, mm)
        w = [hm(h, 60 - mm), hm(mm if mm <= 12 else 12, h * 5 % 60) if mm <= 12 else hm(h, mm + 5), hm(nxt, mm)]
        e = "%d Minuten nach %d Uhr: <b>%s</b>." % (mm, h, ans)
    else:
        mm = R.choice([5, 10, 20])
        word = {5: "fünf", 10: "zehn", 20: "zwanzig"}[mm]
        phrase, ans = "%s vor %s" % (word, ZAHL[nxt]), hm(h, 60 - mm)
        w = [hm(nxt, mm), hm(nxt, 60 - mm), hm(h, mm)]
        e = "%d Minuten vor %s Uhr: <b>%s</b>." % (mm, ZAHL[nxt], ans)
    return mcq("Welche Uhrzeit ist „%s“?" % phrase, ans, [x for x in w if x != ans], e)


def tag24():
    kind = R.choice(["nachm", "nachm", "spaeter", "abends"])
    if kind == "nachm":
        h = R.randint(13, 22)
        m = R.choice([0, 15, 30, 45])
        ans = "%d:%02d Uhr" % (h - 12, m) + (" nachmittags" if h < 18 else " abends")
        w = ["%d:%02d Uhr" % (h - 10, m) + (" nachmittags" if h < 18 else " abends"), "%d:%02d Uhr morgens" % (h - 12, m),
             "%d:%02d Uhr" % ((h - 2) % 12 or 12, m) + (" nachmittags" if h < 18 else " abends")]
        return mcq("Wie sagt man %s im Alltag?" % hm(h, m), ans, [x for x in w if x != ans],
                   "Nach 12 Uhr zählt man weiter: 13 Uhr ist 1 Uhr nachmittags. %d − 12 = %d, also <b>%s</b>." % (h, h - 12, ans))
    if kind == "spaeter":
        h = R.randint(9, 20)
        m = R.choice([0, 10, 15, 30, 45])
        d = R.randint(2, 4)
        r = h + d
        if r > 23:
            return None
        return mcq("Es ist %s. Wie spät ist es %d Stunden später?" % (hm(h, m), d), hm(r, m),
                   [hm(x, m) for x in (r + 1, (r - 12) if r > 12 else r + 12, h + d - 1)] + [hm(h, m + d) if m + d < 60 else None],
                   "%s + %d Stunden = <b>%s</b>." % (hm(h, m), d, hm(r, m)))
    h = R.randint(18, 23)
    v, o = R.choice([("isst", "Abendbrot"), ("geht", "ins Bett"), ("liest", "ein Buch"), ("putzt", "die Zähne")])
    p = KIDS.next()
    q = "%s %s um %d Uhr abends %s. Wie schreibt man diese Uhrzeit mit 24 Stunden?" % (p[0], v, h - 12, o)
    return mcq(q, hm(h, 0), [hm(x, 0) for x in (h - 12, h + 2 if h + 2 < 24 else h - 2, (h - 12) * 2 if (h - 12) * 2 != h else h - 1)],
               "Abends rechnet man 12 Stunden dazu: %d + 12 = <b>%d</b>, also %s." % (h - 12, h, hm(h, 0)))


def spanne():
    h1 = R.randint(7, 16)
    m1 = R.choice([0, 10, 15, 20, 30, 40, 45, 50])
    d = R.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 125])
    t = h1 * 60 + m1 + d
    h2, m2 = divmod(t, 60)
    if h2 > 20:
        return None
    naive = (h2 - h1) * 60 + (m2 - m1) if m2 >= m1 else (h2 - h1) * 100 + m2 - m1
    w = [d + 10, d - 10 if d > 10 else d + 20, naive if naive != d and naive > 0 else d + 60, abs(m2 - m1) + 60 * (h2 - h1) + 40 if m2 < m1 else d + 5]
    return mcq("Von %s bis %s. Wie lange dauert das?" % (hm(h1, m1), hm(h2, m2)), dauer(d), [dauer(x) for x in w if x > 0 and dauer(x) != dauer(d)],
               "Rechne in Schritten: von %s bis %s sind %d min, dann bis %s noch %s. Zusammen <b>%s</b>."
               % (hm(h1, m1), hm(h1 + 1, 0), 60 - m1 if m1 else 60, hm(h2, m2), dauer(t - (h1 + 1) * 60) if t > (h1 + 1) * 60 else "0 min", dauer(d))
               if m1 and t > (h1 + 1) * 60 else "Von %s bis %s sind es <b>%s</b>." % (hm(h1, m1), hm(h2, m2), dauer(d)))


def einheiten():
    kind = R.choice(["hmin", "minh", "tag", "woche", "jahr", "minsek", "gemischt"])
    if kind == "hmin":
        h = R.randint(2, 5)
        return mcq("%d h = ? min" % h, "%d min" % (60 * h), ["%d min" % x for x in (100 * h, 10 * h, 60 * h + 60)], "1 h = 60 min. %d · 60 = <b>%d min</b>." % (h, 60 * h))
    if kind == "minh":
        return mcq("Wie viele Minuten sind eine halbe Stunde?", "30 min", ["50 min", "15 min", "60 min"], "1 h = 60 min, die Hälfte sind <b>30 min</b>.") \
            if R.random() < 0.5 else mcq("Wie viele Minuten sind eine Viertelstunde?", "15 min", ["25 min", "30 min", "45 min"], "60 min : 4 = <b>15 min</b>.")
    if kind == "tag":
        n = R.randint(2, 3)
        return mcq("Wie viele Stunden haben %d Tage?" % n, "%d h" % (24 * n), ["%d h" % x for x in (12 * n, 20 * n, 24 * n + 24)], "1 Tag = 24 h. %d · 24 = <b>%d h</b>." % (n, 24 * n))
    if kind == "woche":
        n = R.randint(2, 5)
        return mcq("Wie viele Tage sind %d Wochen?" % n, "%d Tage" % (7 * n), ["%d Tage" % x for x in (5 * n, 7 * n + 7, 10 * n)], "1 Woche = 7 Tage. %d · 7 = <b>%d Tage</b>." % (n, 7 * n))
    if kind == "jahr":
        return mcq("Wie viele Monate hat ein Jahr?", "12 Monate", ["10 Monate", "52 Monate", "365 Monate"], "Ein Jahr hat <b>12 Monate</b> (und 365 oder 366 Tage).") \
            if R.random() < 0.5 else mcq("Wie viele Monate sind ein halbes Jahr?", "6 Monate", ["5 Monate", "12 Monate", "3 Monate"], "12 : 2 = <b>6 Monate</b>.")
    if kind == "minsek":
        n = R.randint(2, 4)
        return mcq("%d min = ? s" % n, "%d s" % (60 * n), ["%d s" % x for x in (100 * n, 10 * n, 60 * n + 60)], "1 min = 60 s. %d · 60 = <b>%d s</b>." % (n, 60 * n))
    h = R.randint(1, 2)
    m = R.choice([5, 10, 15, 20, 30, 40, 45])
    tot = 60 * h + m
    return mcq("%d h %d min = ? min" % (h, m), "%d min" % tot, ["%d min" % x for x in (100 * h + m, h * 10 + m, tot + 60)],
               "%d h = %d min, dazu %d min: <b>%d min</b>." % (h, 60 * h, m, tot))


def sache():
    p = KIDS.next()
    kind = R.choice(["film", "schule", "kuchen", "bus", "training"])
    if kind == "film":
        h, m = R.randint(15, 18), R.choice([0, 15, 30, 45])
        d = R.choice([75, 85, 90, 95, 100, 105])
        t = h * 60 + m + d
        q = "Ein Kinofilm beginnt um %s und dauert %d Minuten. Wann ist er zu Ende?" % (hm(h, m), d)
        ans = hm(t // 60, t % 60)
        w = [hm(h + 1, m + d - 60) if m + d - 60 < 60 else None, hm(h, (m + d) % 100) if (m + d) % 100 < 60 else hm(h + 2, m), hm((t + 30) // 60, (t + 30) % 60), hm(t // 60 + 1, t % 60)]
        return mcq(q, ans, [x for x in w if x and x != ans], "%d min = %s. %s + %s = <b>%s</b>." % (d, dauer(d), hm(h, m), dauer(d), ans))
    if kind == "schule":
        h1, m1 = 7, R.choice([45, 50, 55])
        h2, m2 = R.choice([11, 12, 13]), R.choice([15, 20, 30, 35])
        d = h2 * 60 + m2 - h1 * 60 - m1
        q = "%s ist von %s bis %s in der Schule. Wie lange ist das?" % (p[0], hm(h1, m1), hm(h2, m2))
        return mcq(q, dauer(d), [dauer(x) for x in (d + 60, d - 20, (h2 - h1) * 60 + abs(m2 - m1)) if x != d and x > 0],
                   "Von %s bis 8:00 Uhr sind %d min, von 8:00 Uhr bis %s sind %s. Zusammen <b>%s</b>." % (hm(h1, m1), 60 - m1, hm(h2, m2), dauer((h2 - 8) * 60 + m2), dauer(d)))
    if kind == "kuchen":
        h, m = R.randint(14, 16), R.choice([10, 20, 35, 40, 50])
        d = R.choice([35, 40, 45, 50, 55])
        t = h * 60 + m + d
        q = "Ein Kuchen kommt um %s in den Ofen und muss %d Minuten backen. Wann ist er fertig?" % (hm(h, m), d)
        ans = hm(t // 60, t % 60)
        w = [hm(h, (m + d) % 60), hm(t // 60 + 1, t % 60), hm((t - 10) // 60, (t - 10) % 60), hm((t + 10) // 60, (t + 10) % 60)]
        return mcq(q, ans, [x for x in w if x != ans], "%s + %d min = <b>%s</b>." % (hm(h, m), d, ans))
    if kind == "bus":
        h, m = R.randint(7, 17), R.choice([5, 12, 18, 25, 33, 41, 48])
        late = R.choice([5, 10, 15, 20])
        t = h * 60 + m + late
        q = "Der Bus sollte um %s abfahren. Er hat %d Minuten Verspätung. Wann fährt er ab?" % (hm(h, m), late)
        ans = hm(t // 60, t % 60)
        return mcq(q, ans, [hm((t - 2 * late) // 60, (t - 2 * late) % 60), hm(t // 60, (t % 60 + 10) % 60), hm(t // 60 + 1, t % 60)],
                   "%s + %d min = <b>%s</b>." % (hm(h, m), late, ans))
    n = R.randint(2, 5)
    d = R.choice([30, 45, 60, 90])
    tot = n * d
    q = "%s trainiert %d-mal in der Woche je %d Minuten Fußball. Wie lange ist das zusammen?" % (p[0], n, d)
    return mcq(q, dauer(tot), [dauer(x) for x in (tot + d, tot - d, n + d) if x != tot and x > 0],
               "%d · %d min = %d min = <b>%s</b>." % (n, d, tot, dauer(tot)))


def main():
    seen = set()
    sets = [
        ("Die Uhr ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Uhrzeiten in Worten", mix(R, seen, [(worte, 20)])),
        ("Vormittag, Nachmittag und 24 Stunden", mix(R, seen, [(tag24, 20)])),
        ("Zeitspannen", mix(R, seen, [(spanne, 14), (einheiten, 6)])),
        ("Sachaufgaben zur Zeit", mix(R, seen, [(sache, 14), (einheiten, 6)])),
    ]
    body = lesson(
        ["Der <b>kurze Zeiger</b> zeigt die Stunden, der <b>lange Zeiger</b> die Minuten.",
         "„Halb vier“ heißt eine halbe Stunde <b>vor</b> vier Uhr, also 3:30 Uhr. „Viertel nach drei“ ist 3:15 Uhr, „Viertel vor vier“ ist 3:45 Uhr.",
         "Ein Tag hat 24 Stunden. Nach 12 Uhr mittags zählt man weiter: 3 Uhr nachmittags = 15 Uhr.",
         "Eine <b>Zeitspanne</b> rechnest du in Schritten, am besten bis zur vollen Stunde: 8:40 Uhr → 9:00 Uhr (20 min) → 9:25 Uhr (25 min)."],
        [example("Wie lange dauert es von 8:40 Uhr bis 10:15 Uhr?", ["8:40 → 9:00 Uhr: 20 min", "9:00 → 10:00 Uhr: 1 h", "10:00 → 10:15 Uhr: 15 min"], "1 h 35 min"),
         example("Welche Uhrzeit ist „halb acht“?", ["eine halbe Stunde vor acht Uhr"], "7:30 Uhr (oder 19:30 Uhr)")],
        [["„Halb vier“ = 4:30 Uhr", "„Halb vier“ = 3:30 Uhr"],
         ["1 h = 100 min", "1 h = 60 min"],
         ["Von 8:40 bis 9:10 Uhr = 70 min", "Bis zur vollen Stunde rechnen: 20 min + 10 min = 30 min"]],
        extra=table(["Einheit", "Umrechnung"], [["1 Minute", "60 Sekunden"], ["1 Stunde", "60 Minuten"], ["1 Tag", "24 Stunden"], ["1 Woche", "7 Tage"], ["1 Jahr", "12 Monate"]]))
    faq = [
        {"q": "Warum ist „halb vier“ 3:30 Uhr?", "a": "Im Deutschen bezieht sich „halb“ auf die kommende Stunde: halb vier ist die Hälfte des Weges zu vier Uhr, also 3:30 Uhr."},
        {"q": "Wie rechnet man Zeitspannen?", "a": "In Schritten: zuerst bis zur nächsten vollen Stunde, dann die vollen Stunden, dann die restlichen Minuten."},
        {"q": "Wann lernt man die 24-Stunden-Zählung?", "a": "Meist in Klasse 2 oder 3. Fahrpläne und digitale Uhren zeigen die Zeiten von 0:00 bis 23:59 Uhr."},
        {"q": "Wie schreibt man Uhrzeiten?", "a": "Zum Beispiel 8:15 Uhr oder 8.15 Uhr. Für Zeitspannen schreibt man h (Stunden) und min (Minuten)."},
    ]
    make_unit(R, "uhrzeit-und-zeitspannen", "G",
              "Die Schülerinnen und Schüler lesen Uhrzeiten ab, nutzen die 24-Stunden-Zählung, berechnen Zeitspannen und rechnen mit Zeiteinheiten in Sachsituationen (Zusammenfassung).",
              "Uhrzeit und Zeitspannen",
              "Uhrzeit Klasse 3 – Uhr lesen und Zeitspannen, Arbeitsblätter mit Lösungen",
              "Uhrzeit und Zeitspannen",
              "Uhrzeit für Klasse 3: Uhr ablesen, halb und Viertel, 24 Stunden, Zeitspannen berechnen, Zeiteinheiten und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "„Halb vier“ ist 3:30 Uhr.",
              "Zeitspannen rechnest du in Schritten bis zur vollen Stunde.",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
